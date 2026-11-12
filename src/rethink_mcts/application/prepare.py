"""
Dataset Preparation Service matching §11 of spec.
Converts raw datasets into separated public and hidden stores:
prepared/<dataset>/
  manifest.json
  public/problems.jsonl
  judge/suites/<problem_id>.json
"""

import os
import json
import logging
import hashlib
from pathlib import Path
import inspect
from dataclasses import asdict
from typing import Optional, List, Dict, Any

from rethink_mcts.domain.problem import PublicProblem, HiddenProblem, TestCase, StdinCase, FunctionCase, AssertionSuite
from rethink_mcts.adapters.datasets.humaneval import parse_humaneval_record
from rethink_mcts.adapters.datasets.apps import parse_apps_record
from rethink_mcts.adapters.datasets.code_contests import parse_code_contests_record

logger = logging.getLogger(__name__)


def serialize_test_case(c: TestCase) -> Dict[str, Any]:
    if isinstance(c, StdinCase):
        return {
            "stdin": c.stdin,
            "expected_stdout": c.expected_stdout,
            "case_id": c.case_id,
            "comparator_id": c.comparator_id
        }
    elif isinstance(c, FunctionCase):
        return {
            "entry_point": c.entry_point,
            "args": list(c.args),
            "kwargs": dict(c.kwargs),
            "expected": c.expected,
            "case_id": c.case_id
        }
    elif isinstance(c, AssertionSuite):
        return {
            "test_code": c.test_code,
            "entry_point": c.entry_point,
            "case_id": c.case_id
        }
    return {}


def serialize_public_problem(p: PublicProblem) -> Dict[str, Any]:
    spec = {
        "mode": p.execution_spec.mode.value if hasattr(p.execution_spec.mode, "value") else str(p.execution_spec.mode),
        "entry_point": p.execution_spec.entry_point
    }
    if p.execution_spec.starter_code:
        spec["starter_code"] = p.execution_spec.starter_code
    return {
        "problem_id": p.problem_id,
        "statement": p.statement,
        "execution_spec": spec,
        "public_tests": [serialize_test_case(c) for c in p.public_tests],
        "limits": {
            "timeout_seconds": p.limits.timeout_seconds,
            "memory_mb": p.limits.memory_mb,
            "stdout_limit_bytes": p.limits.stdout_limit_bytes
        },
        "metadata": {
            "source": p.metadata.source,
            "split": p.metadata.split,
            "difficulty": p.metadata.difficulty,
            "cf_rating": p.metadata.cf_rating
        }
    }


def serialize_hidden_problem(h: HiddenProblem) -> Dict[str, Any]:
    return {
        "problem_id": h.problem_id,
        "hidden_suite": {
            "suite_id": h.hidden_suite.suite_id,
            "cases": [serialize_test_case(c) for c in h.hidden_suite.cases],
            "generated_cases": [serialize_test_case(c) for c in h.hidden_suite.generated_cases]
        },
        "judge_spec": {
            "timeout_seconds": h.judge_spec.timeout_seconds,
            "comparator_id": h.judge_spec.comparator_id
        }
    }


def prepare_dataset(
    dataset_name: str,
    raw_path: Optional[str] = None,
    output_dir: Optional[str] = None,
    limit: Optional[int] = None,
    public_split: str = "first_two"
) -> Dict[str, Any]:
    """
    Prepares dataset and writes separated public and judge stores.
    """
    dataset_name = dataset_name.lower()
    out_base = output_dir or os.path.join("prepared", dataset_name)
    public_dir = os.path.join(out_base, "public")
    judge_suites_dir = os.path.join(out_base, "judge", "suites")
    os.makedirs(public_dir, exist_ok=True)
    os.makedirs(judge_suites_dir, exist_ok=True)

    public_jsonl_path = os.path.join(public_dir, "problems.jsonl")

    records: List[Dict[str, Any]] = []

    if dataset_name == "humaneval":
        src = raw_path or "data/humaneval/processed.jsonl"
        if not os.path.exists(src):
            import requests
            os.makedirs(os.path.dirname(src), exist_ok=True)
            url = "https://raw.githubusercontent.com/SIMONLQY/RethinkMCTS/master/dataProcess/humaneval/processed.jsonl"
            resp = requests.get(url, timeout=30)
            if resp.ok:
                with open(src, "w", encoding="utf-8") as f:
                    f.write(resp.text)
            else:
                raise RuntimeError(f"Failed to fetch HumanEval from upstream: {resp.status_code}")

        with open(src, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line.strip()))

        parser_fn = parse_humaneval_record

    elif dataset_name == "apps":
        src = raw_path or "data/apps/sample_apps.jsonl"
        if not os.path.exists(src):
            raise FileNotFoundError(f"APPS source file not found at {src}. Please provide raw_path.")

        with open(src, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line.strip()))

        parser_fn = parse_apps_record

    elif dataset_name == "code_contests":
        src = raw_path or "prepared/code_contests/raw.jsonl"
        if not os.path.exists(src):
            raise FileNotFoundError(f"CodeContests raw source not found at {src}")
        with open(src, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line.strip()))
        parser_fn = parse_code_contests_record

    else:
        raise ValueError(f"Unsupported dataset: {dataset_name}. Must be 'humaneval', 'apps', or 'code_contests'.")

    if limit is not None and limit > 0:
        records = records[:limit]

    prepared_count = 0
    public_count = hidden_count = 0
    with open(public_jsonl_path, "w", encoding="utf-8") as pub_out:
        for item in records:
            pub_prob, hid_prob = parser_fn(item, public_split) if dataset_name == "apps" else parser_fn(item)
            pub_out.write(json.dumps(serialize_public_problem(pub_prob)) + "\n")

            # Save hidden suite
            hid_path = os.path.join(judge_suites_dir, f"{hid_prob.problem_id}.json")
            with open(hid_path, "w", encoding="utf-8") as hid_out:
                json.dump(serialize_hidden_problem(hid_prob), hid_out, indent=2)

            prepared_count += 1
            public_count += len(pub_prob.public_tests)
            hidden_count += len(hid_prob.hidden_suite.cases)

    manifest = {
        "dataset": dataset_name,
        "total_problems": prepared_count,
        "public_problems_path": public_jsonl_path,
        "judge_suites_dir": judge_suites_dir,
        "schema_version": 2,
        "source_path": src,
        "source_sha256": hashlib.sha256(Path(src).read_bytes()).hexdigest(),
        "adapter_sha256": hashlib.sha256(Path(inspect.getfile(parser_fn)).read_bytes()).hexdigest(),
        "public_case_count": public_count,
        "hidden_case_count": hidden_count,
        "protocol": ("first_two_public_remove_cross_split_duplicates" if public_split == "first_two"
                     else f"{public_split}_of_distinct_tests_public") if dataset_name == "apps" else "adapter_public_hidden",
        "public_split": public_split if dataset_name == "apps" else None,
        "provenance": "Locally prepared source; protocol equivalence to paper is not asserted"
    }

    with open(os.path.join(out_base, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest
