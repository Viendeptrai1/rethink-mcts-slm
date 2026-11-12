"""
APPS dataset adapter matching paper (§11.3).
Supports introductory, interview, and competition splits with call-based and stdin modes.
"""

import json
from rethink_mcts.domain.errors import ConfigurationError
from typing import Tuple, List, Union
from dataclasses import asdict
from rethink_mcts.domain.problem import (
    PublicProblem,
    HiddenProblem,
    HiddenSuite,
    StdinCase,
    FunctionCase,
    ExecutionSpec,
    ExecutionMode,
    ProblemLimits,
    PublicMetadata,
    JudgeSpec
)


PUBLIC_SPLITS = ("first_two", "half", "half_min2")


def public_count_for(total: int, public_split: str) -> int:
    """Number of leading tests used as public tests.

    first_two: the v1 protocol (first 2 tests public).
    half: upstream RethinkMCTS `--public-cases-type half` (floor(total / 2)).
    half_min2: floor(total / 2) but at least 2 (7B branch option).
    """
    if public_split == "first_two":
        return 2
    if public_split == "half":
        return total // 2
    if public_split == "half_min2":
        return max(2, total // 2)
    raise ConfigurationError(f"Unknown APPS public split: {public_split}")


def parse_apps_record(item: dict, public_split: str = "first_two") -> Tuple[PublicProblem, HiddenProblem]:
    """
    Parses an APPS record:
    {
      "id": 0 (or "problem_id": 0),
      "question": "...",
      "input_output": "{\"inputs\": [...], \"outputs\": [...], \"fn_name\": ...}",
      "difficulty": "introductory" | "interview" | "competition"
    }
    """
    raw_id = item.get("id", item.get("problem_id", 0))
    prob_id = f"apps_{raw_id}"
    question = item.get("question", "")
    difficulty = item.get("difficulty", "introductory")

    io_data = {}
    io_str = item.get("input_output", "")
    if isinstance(io_str, str) and io_str.strip():
        try:
            io_data = json.loads(io_str)
        except Exception:
            io_data = {}
    elif isinstance(io_str, dict):
        io_data = io_str

    fn_name = io_data.get("fn_name")
    inputs = io_data.get("inputs", [])
    outputs = io_data.get("outputs", [])

    if len(inputs) != len(outputs):
        raise ConfigurationError(f"{prob_id}: input/output counts differ")
    if public_split not in PUBLIC_SPLITS:
        raise ConfigurationError(f"Unknown APPS public split: {public_split}")
    if public_split == "first_two" and len(inputs) < 3:
        raise ConfigurationError(f"{prob_id}: need at least 3 tests for disjoint public/hidden split")

    all_cases: List[Union[StdinCase, FunctionCase]] = []

    if fn_name:
        # Call-based / Function mode
        mode = ExecutionMode.FUNCTION
        for idx, (inp, out) in enumerate(zip(inputs, outputs)):
            args = tuple(inp) if isinstance(inp, list) else (inp,)
            all_cases.append(
                FunctionCase(
                    entry_point=fn_name,
                    args=args,
                    expected=out,
                    case_id=f"case_{idx+1}"
                )
            )
    else:
        # Standard input / output mode
        mode = ExecutionMode.STDIN
        for idx, (inp, out) in enumerate(zip(inputs, outputs)):
            inp_text = "\n".join(inp) if isinstance(inp, list) else str(inp)
            out_text = "\n".join(out) if isinstance(out, list) else str(out)
            all_cases.append(
                StdinCase(
                    stdin=inp_text + "\n" if not inp_text.endswith("\n") else inp_text,
                    expected_stdout=out_text + "\n" if not out_text.endswith("\n") else out_text,
                    case_id=f"case_{idx+1}"
                )
            )

    def case_key(case):
        return json.dumps({k: v for k, v in asdict(case).items() if k != "case_id"}, sort_keys=True)
    if public_split == "first_two":
        # v1 protocol: first 2 cases public, later duplicates of them dropped from the hidden suite.
        split_cases = all_cases
    else:
        # Split the *distinct* tests, so a problem whose suite repeats tests still keeps
        # genuinely unseen hidden tests (e.g. apps_4349 lists 5 distinct tests twice).
        seen, split_cases = set(), []
        for case in all_cases:
            if case_key(case) not in seen:
                seen.add(case_key(case))
                split_cases.append(case)
    n_public = public_count_for(len(split_cases), public_split)
    if n_public < 1 or n_public >= len(split_cases):
        raise ConfigurationError(
            f"{prob_id}: cannot split {len(split_cases)} distinct tests into public/hidden with '{public_split}'")
    # Leading cases are public examples for search; the remainder are hidden tests for the judge
    pub_cases = tuple(split_cases[:n_public])
    public_keys = {case_key(c) for c in pub_cases}
    hid_cases = tuple(c for c in split_cases[n_public:] if case_key(c) not in public_keys)
    if not hid_cases:
        raise ConfigurationError(f"{prob_id}: no hidden cases remain after removing public duplicates")

    public_problem = PublicProblem(
        problem_id=prob_id,
        statement=question,
        execution_spec=ExecutionSpec(mode=mode, entry_point=fn_name,
                                     starter_code=(item.get("starter_code") or None)),
        public_tests=pub_cases,
        limits=ProblemLimits(timeout_seconds=4.0),
        metadata=PublicMetadata(source="APPS", difficulty=difficulty)
    )

    hidden_problem = HiddenProblem(
        problem_id=prob_id,
        hidden_suite=HiddenSuite(cases=hid_cases, suite_id=f"{prob_id}_hidden"),
        judge_spec=JudgeSpec(timeout_seconds=4.0)
    )

    return public_problem, hidden_problem
