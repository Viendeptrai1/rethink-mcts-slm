from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from baselines.direct_generation.pipeline import safe_path_component
from baselines.sample_selection import load_sample_manifest, problem_keys
from evaluation.batch_evaluation import discover_candidates


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLES = {
    "apps": Path("data/samples/benchmark_v2/apps_test_300.json"),
    "humaneval": Path("data/samples/benchmark_v2/humaneval_test_164.json"),
}
GENERATION_FIELDS = ("prompt_version", "max_tokens", "temperature", "top_p", "reasoning_effort", "seed")
INDEX_FIELDS = (
    "dataset", "problem_id", "candidate_path", "solution_sha256", "generation_run",
    "requested_model", "response_model", "finish_reason", "prompt_version",
    "max_tokens", "temperature", "top_p", "reasoning_effort", "seed", "prompt_tokens",
    "completion_tokens", "total_tokens", "failure_type", "passed_tests", "total_tests",
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _rows(path: Path) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(path)
    rows: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            key = str(row["problem_id"])
            if key in rows:
                raise ValueError(f"Duplicate result for {key}: {path}")
            rows[key] = row
    return rows


def _code_fingerprint(root: Path) -> str:
    files = []
    for directory in ("DataProcess", "Executors", "baselines", "evaluation", "tools/remote_evaluation"):
        files.extend((root / directory).rglob("*.py"))
    files.extend((root / "tools/remote_evaluation" / name) for name in ("Dockerfile", "requirements.txt", "run.sh"))
    digest = hashlib.sha256()
    for path in sorted(files):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _test_data_fingerprint(root: Path, dataset: str, ids: list[int]) -> str:
    if dataset == "apps":
        files = [root / "data/apps/raw/test" / f"{value:04d}" / "input_output.json" for value in ids]
    else:
        files = sorted(path for path in (root / "data/humaneval/arrow").rglob("*") if path.is_file())
    if not files:
        raise FileNotFoundError(f"No test data found for {dataset}")
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def create_record(
    *,
    root: Path,
    bundle_file: Path,
    method: str = "Direct Evaluation",
    execution_site: str = "ckey_gpu",
) -> Path:
    root = root.resolve()
    bundle = json.loads(bundle_file.read_text(encoding="utf-8"))
    run_name = str(bundle["run_name"])
    model = str(bundle["model"])
    run_dir = safe_path_component(run_name)
    model_dir = safe_path_component(model)
    if run_dir != run_name:
        raise ValueError("Unsafe benchmark run name")
    evaluation_dir = root / "outputs/baselines/evaluations" / run_dir / model_dir
    judge_path = evaluation_dir / "benchmark_summary.json"
    judge = json.loads(judge_path.read_text(encoding="utf-8"))
    if judge.get("run_name") != run_name or judge.get("model") != model:
        raise ValueError("Judge summary belongs to another run or model")

    cohorts: dict[str, Any] = {}
    evaluations: dict[str, Any] = {}
    coverage: dict[str, Any] = {}
    all_index: list[dict[str, Any]] = []
    generation_profiles: set[str] = set()
    source_files = [judge_path, evaluation_dir / "benchmark_table.csv", evaluation_dir / "benchmark_table.md"]
    for dataset, relative in SAMPLES.items():
        sample_path = root / relative
        manifest = load_sample_manifest(sample_path, dataset=dataset)
        expected_ids = [f"{value:04d}" if dataset == "apps" else f"HumanEval/{value}" for value in manifest["problem_ids"]]
        results_path = evaluation_dir / dataset / "results.jsonl"
        summary_path = evaluation_dir / dataset / "summary.json"
        results = _rows(results_path)
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        config = summary.get("evaluation_config") or {}
        sample_hash = _sha256(sample_path)
        if config.get("sample_manifest_sha256") != sample_hash or config.get("sample_manifest") is None:
            raise ValueError(f"Evaluation configuration does not match the {dataset} cohort")
        if config.get("max_tests") is not None or config.get("split") != "test":
            raise ValueError(f"Nonstandard evaluation scope for {dataset}")
        expected_policy = "all_input_output_cases" if dataset == "apps" else "official_harness"
        expected_timeout_scope = "per_test" if dataset == "apps" else "official_harness"
        if config.get("test_policy") != expected_policy or config.get("timeout_scope") != expected_timeout_scope:
            raise ValueError(f"Nonstandard test policy for {dataset}")
        if summary.get("run_name") != run_name or summary.get("model") != model:
            raise ValueError(f"Evaluation summary belongs to another run or model: {dataset}")
        missing = sorted(set(expected_ids) - set(results))
        extras = sorted(set(results) - set(expected_ids))
        infra_errors = sorted(key for key, row in results.items() if row.get("failure_type") == "executor_error")
        zero_tests = sorted(key for key, row in results.items() if int(row.get("total_tests") or 0) <= 0)
        if missing or extras or infra_errors or zero_tests:
            raise ValueError(f"{dataset} incomplete: missing={len(missing)}, extra={len(extras)}, executor_errors={len(infra_errors)}, zero_tests={len(zero_tests)}")

        candidates = discover_candidates(
            output_dir=root / "outputs/baselines", run_name=run_name, dataset=dataset,
            model=model, split="test", selected_problem_keys=problem_keys(sample_path, dataset=dataset),
        )
        by_id = {candidate.problem_id: candidate for candidate in candidates}
        candidate_missing = sorted(set(expected_ids) - set(by_id))
        if candidate_missing:
            raise ValueError(f"{dataset} has {len(candidate_missing)} missing generated candidates")
        for problem_id in expected_ids:
            candidate = by_id[problem_id]
            solution_hash = _sha256(candidate.artifact_dir / "solution.py")
            candidate_report = json.loads((candidate.artifact_dir / "evaluation.json").read_text(encoding="utf-8"))
            provenance = candidate_report.get("evaluation_provenance") or {}
            expected_provenance = {
                "solution_sha256": solution_hash,
                "timeout_seconds": config["timeout_seconds"],
                "test_workers": config["test_workers"],
                "max_tests": config["max_tests"],
            }
            if provenance != expected_provenance:
                raise ValueError(f"Candidate {dataset}/{problem_id} was evaluated with different code or settings")
            if any(candidate_report.get(field) != results[problem_id].get(field) for field in ("passed_tests", "total_tests")):
                raise ValueError(f"Candidate {dataset}/{problem_id} report differs from aggregate")
            metadata = json.loads((candidate.artifact_dir / "metadata.json").read_text(encoding="utf-8"))
            generation = metadata.get("generation") or {}
            profile = {field: generation.get(field) for field in GENERATION_FIELDS}
            generation_profiles.add(json.dumps(profile, sort_keys=True))
            usage = metadata.get("usage") or {}
            result = results[problem_id]
            all_index.append({
                "dataset": dataset,
                "problem_id": problem_id,
                "candidate_path": candidate.artifact_dir.relative_to(root).as_posix(),
                "solution_sha256": solution_hash,
                "generation_run": metadata.get("run_name"),
                "requested_model": metadata.get("requested_model"),
                "response_model": metadata.get("response_model"),
                "finish_reason": metadata.get("finish_reason"),
                **profile,
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
                "failure_type": result.get("failure_type"),
                "passed_tests": result.get("passed_tests"),
                "total_tests": result.get("total_tests"),
            })
        cohorts[dataset] = {
            "sample_id": manifest["sample_id"],
            "seed": manifest.get("seed"),
            "manifest": relative.as_posix(),
            "manifest_sha256": sample_hash,
            "test_data_sha256": _test_data_fingerprint(root, dataset, manifest["problem_ids"]),
            "size": len(expected_ids),
            "difficulty_counts": judge["datasets"][dataset]["groups"]["overall"].get("difficulty_counts"),
        }
        evaluations[dataset] = {**config, "wall_time_seconds": summary.get("wall_time_seconds")}
        coverage[dataset] = {"expected": len(expected_ids), "evaluated": len(results), "missing": 0, "executor_errors": 0}
        judge_dataset = judge["datasets"][dataset]
        if (
            judge_dataset["sample_manifest"].get("problem_ids") != manifest["problem_ids"]
            or judge_dataset["groups"]["overall"].get("expected_candidates") != len(expected_ids)
        ):
            raise ValueError(f"Judge report does not match the {dataset} cohort")
        source_files.extend([results_path, summary_path])

    if judge.get("method") != method or judge.get("table", {}).get("Method") != method:
        raise ValueError("Judge method label does not match the benchmark method")
    if judge["datasets"]["apps"]["groups"]["overall"]["missing_candidates"] or judge["datasets"]["humaneval"]["groups"]["overall"]["missing_candidates"]:
        raise ValueError("Judge report contains missing candidates")
    execution = {
        "site": execution_site,
        "backend": os.getenv("EVALUATION_BACKEND", "unknown"),
        "image_id": os.getenv("EVALUATION_IMAGE_ID"),
        "cpu_limit": os.getenv("EVALUATION_CPU_LIMIT"),
        "memory_limit": os.getenv("EVALUATION_MEMORY_LIMIT"),
        "pids_limit": os.getenv("EVALUATION_PIDS_LIMIT"),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "code_sha256": _code_fingerprint(root),
    }
    source_hashes = {path.relative_to(root).as_posix(): _sha256(path) for path in source_files}
    source_hashes["candidate_index"] = hashlib.sha256(json.dumps(all_index, sort_keys=True).encode("utf-8")).hexdigest()
    source_hashes["bundle"] = _sha256(bundle_file)
    source_hashes["record_context"] = hashlib.sha256(json.dumps({
        "method": method, "provider": bundle.get("provider"), "model_revision": bundle.get("model_revision"),
        "source_run": bundle.get("source_run"),
        "cohorts": cohorts, "execution": execution,
    }, sort_keys=True).encode("utf-8")).hexdigest()
    fingerprint = hashlib.sha256(json.dumps(source_hashes, sort_keys=True).encode("utf-8")).hexdigest()
    target = root / "outputs/benchmarks" / run_dir / model_dir
    if target.exists():
        previous = json.loads((target / "run.json").read_text(encoding="utf-8"))
        if previous.get("source_fingerprint") == fingerprint:
            return target
        raise FileExistsError(f"Benchmark record already exists with different inputs: {target}")

    record = {
        "schema_version": 1,
        "status": "complete",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_name": run_name,
        "method": method,
        "model": model,
        "model_revision": bundle.get("model_revision"),
        "provider": bundle.get("provider"),
        "source_generation_run": bundle.get("source_run"),
        "bundle_sha256": _sha256(bundle_file),
        "cohorts": cohorts,
        "generation_profiles": [json.loads(value) for value in sorted(generation_profiles)],
        "evaluation": evaluations,
        "coverage": coverage,
        "execution": execution,
        "metrics": judge["table"],
        "source_hashes": source_hashes,
        "source_fingerprint": fingerprint,
    }

    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{model_dir}.", dir=target.parent))
    try:
        (staging / "run.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        with (staging / "candidates.csv").open("w", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=INDEX_FIELDS)
            writer.writeheader()
            writer.writerows(all_index)
        shutil.copy2(evaluation_dir / "benchmark_table.csv", staging / "benchmark_table.csv")
        shutil.copy2(evaluation_dir / "benchmark_table.md", staging / "benchmark_table.md")
        shutil.copy2(judge_path, staging / "benchmark_summary.json")
        for dataset, relative in SAMPLES.items():
            dataset_dir = staging / dataset
            dataset_dir.mkdir()
            shutil.copy2(root / relative, dataset_dir / "sample_manifest.json")
            for filename in ("summary.json", "results.jsonl", "results.csv", "failures.csv", "evaluation.log", "benchmark_metrics.json"):
                source = evaluation_dir / dataset / filename
                if source.is_file():
                    shutil.copy2(source, dataset_dir / filename)
        staging.rename(target)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freeze a completed benchmark with its actual parameters and provenance")
    parser.add_argument("--bundle-file", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--method", default="Direct Evaluation")
    parser.add_argument("--execution-site", default="ckey_gpu")
    args = parser.parse_args(argv)
    print(create_record(root=args.root, bundle_file=args.bundle_file, method=args.method, execution_site=args.execution_site))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
