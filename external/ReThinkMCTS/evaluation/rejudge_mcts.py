from __future__ import annotations

import argparse
import hashlib
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from baselines.direct_generation.pipeline import safe_path_component
from baselines.sample_selection import load_problem_ids
from evaluation.batch_evaluation import Candidate, _evaluate_candidate, _write_aggregate
from evaluation.benchmark_judge import build_dataset_metrics


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APPS_SAMPLE = ROOT / "data" / "samples" / "benchmark_v2" / "apps_test_300.json"
DEFAULT_HUMANEVAL_SAMPLE = ROOT / "data" / "samples" / "benchmark_v2" / "humaneval_test_164.json"


def _key(dataset: str, problem_id: int) -> str:
    return f"{problem_id:04d}" if dataset == "apps" else f"HumanEval/{problem_id}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rejudge final MCTS solutions without rerunning search or LLM calls.")
    parser.add_argument("--dataset", required=True, choices=("apps", "humaneval"))
    parser.add_argument("--source-run-name", required=True)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--sample-file", type=Path, default=None)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--confirm-full-run", action="store_true")
    args = parser.parse_args(argv)
    if args.workers < 1 or args.timeout <= 0:
        parser.error("--workers and --timeout must be greater than zero")
    if args.source_run_name == args.run_name:
        parser.error("Use a distinct --run-name for rejudge artifacts")
    args.sample_file = (args.sample_file or (DEFAULT_APPS_SAMPLE if args.dataset == "apps" else DEFAULT_HUMANEVAL_SAMPLE)).resolve()
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ids = load_problem_ids(args.sample_file, dataset=args.dataset)
    source = ROOT / "outputs" / "rethinkmcts" / safe_path_component(args.source_run_name) / safe_path_component(args.model) / args.dataset
    output = ROOT / "outputs" / "rethinkmcts_evaluations" / "evaluations" / safe_path_component(args.run_name) / safe_path_component(args.model) / args.dataset
    candidates: list[Candidate] = []
    missing: list[str] = []
    for problem_id in ids:
        problem_key = _key(args.dataset, problem_id)
        artifact = source / safe_path_component(problem_key)
        solution = artifact / "final_solution.py"
        summary = artifact / "search_summary.json"
        if not solution.is_file() or not summary.is_file():
            missing.append(problem_key)
            continue
        candidates.append(Candidate(args.dataset, problem_key, "test", artifact, ""))

    config = {
        "source_run_name": args.source_run_name,
        "model": args.model,
        "dataset": args.dataset,
        "test_policy": "all_input_output_cases" if args.dataset == "apps" else "official_harness",
        "timeout_seconds": args.timeout,
        "sample_manifest": str(args.sample_file),
        "sample_manifest_sha256": hashlib.sha256(args.sample_file.read_bytes()).hexdigest(),
    }
    config_path = output / "evaluation_config.json"
    if config_path.is_file() and json.loads(config_path.read_text(encoding="utf-8")) != config:
        raise SystemExit(f"Rejudge configuration changed; use a new --run-name: {config_path}")

    def report_path(candidate: Candidate) -> Path:
        return output / "candidates" / safe_path_component(candidate.problem_id) / "evaluation.json"

    pending = [candidate for candidate in candidates if not report_path(candidate).is_file()]
    print(f"Dataset: {args.dataset}")
    print(f"Source MCTS run: {args.source_run_name}")
    print(f"Final evaluation policy: {config['test_policy']}")
    print(f"Expected: {len(ids)}; candidates: {len(candidates)}; missing: {len(missing)}; pending: {len(pending)}")
    print(f"Output: {output}")
    if args.plan:
        return 0
    if len(ids) > 20 and not args.confirm_full_run:
        raise SystemExit("Run with --plan, then pass --confirm-full-run")
    output.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    started_at = datetime.now(timezone.utc)
    started_clock = time.perf_counter()
    payloads = [{
        **candidate.__dict__, "artifact_dir": str(candidate.artifact_dir),
        "solution_path": str(candidate.artifact_dir / "final_solution.py"),
        "report_path": str(report_path(candidate)), "apps_test_policy": "all",
        "timeout": args.timeout, "test_workers": 1, "max_tests": None, "resume": True,
    } for candidate in pending]
    rows: dict[str, dict] = {}
    executor_errors = 0
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(_evaluate_candidate, payload) for payload in payloads]
        for position, future in enumerate(as_completed(futures), start=1):
            row = future.result()
            rows[row["problem_id"]] = row
            executor_errors += row["failure_type"] == "executor_error"
            print(f"[{position}/{len(payloads)}] {row['problem_id']}: {row['passed_tests']}/{row['total_tests']} ({row['failure_type']})", flush=True)
    for candidate in candidates:
        if candidate.problem_id in rows:
            continue
        path = report_path(candidate)
        if path.is_file():
            payload = {
                **candidate.__dict__, "artifact_dir": str(candidate.artifact_dir),
                "solution_path": str(candidate.artifact_dir / "final_solution.py"),
                "report_path": str(path), "apps_test_policy": "all", "timeout": args.timeout,
                "test_workers": 1, "max_tests": None, "resume": True,
            }
            row = _evaluate_candidate(payload)
            rows[row["problem_id"]] = row
            executor_errors += row["failure_type"] == "executor_error"
    summary = _write_aggregate(
        aggregate_dir=output, rows=list(rows.values()), run_name=args.run_name,
        model=args.model, dataset=args.dataset, workers=args.workers,
        evaluation_config=config | {"missing_problem_ids": missing},
    )
    summary.update({
        "expected_candidates": len(ids), "missing_candidates": len(missing),
        "missing_problem_ids": missing, "started_at_utc": started_at.isoformat(),
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "wall_time_seconds": round(time.perf_counter() - started_clock, 3),
    })
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    metrics = build_dataset_metrics(
        dataset=args.dataset, sample_path=args.sample_file,
        results_path=output / "results.jsonl", run_name=args.run_name, model=args.model,
    )
    (output / "benchmark_metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 1 if executor_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
