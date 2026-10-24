from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from baselines.sample_selection import problem_keys
from baselines.direct_generation.pipeline import is_complete_artifact, safe_path_component


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "baselines"
LARGE_RUN_THRESHOLD = 20


@dataclass(frozen=True)
class Candidate:
    dataset: str
    problem_id: str
    split: str
    artifact_dir: Path
    created_at: str


def parse_args(
    argv: list[str] | None = None, *, dataset: str | None = None
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate a generated run with parallel candidate workers."
    )
    if dataset is None:
        parser.add_argument("--dataset", required=True, choices=("apps", "humaneval"))
    else:
        parser.set_defaults(dataset=dataset)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--source-run-name", default=None, help="Generation run containing immutable solutions.")
    parser.add_argument("--apps-test-policy", choices=("all", "private_half"), default="all")
    parser.add_argument("--model", default=None)
    parser.add_argument("--split", default="test", choices=("train", "test"))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    parser.add_argument(
        "--test-workers",
        type=int,
        default=1,
        help="APPS tests to execute concurrently inside each candidate worker.",
    )
    parser.add_argument("--timeout", type=float, default=None)
    parser.add_argument("--max-tests", type=int, default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--sample-file",
        type=Path,
        default=None,
        help="Immutable JSON manifest restricting evaluation to exact problem IDs.",
    )
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--confirm-full-run", action="store_true")
    args = parser.parse_args(argv)
    if args.workers <= 0:
        parser.error("--workers must be greater than zero")
    if args.test_workers <= 0:
        parser.error("--test-workers must be greater than zero")
    if args.timeout is not None and args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    if args.limit is not None and args.limit <= 0:
        parser.error("--limit must be greater than zero")
    if args.max_tests is not None and args.max_tests <= 0:
        parser.error("--max-tests must be greater than zero")
    if args.dataset == "humaneval" and args.max_tests is not None:
        parser.error("--max-tests only applies to APPS")
    if args.apps_test_policy == "private_half" and args.max_tests is not None:
        parser.error("--max-tests cannot be combined with private_half")
    if args.source_run_name is not None and args.source_run_name == args.run_name:
        parser.error("--source-run-name must differ from --run-name")
    args.output_dir = args.output_dir.resolve()
    if args.sample_file is not None:
        args.sample_file = args.sample_file.resolve()
    return args


def _target_model(explicit_model: str | None) -> str:
    load_dotenv(PROJECT_ROOT / ".env")
    provider = os.getenv("LLM_PROVIDER", "modal").strip().lower()
    configured_name = "LLM_MODEL" if provider == "ollama" else "KIMI_MODEL"
    model = explicit_model or os.getenv(configured_name)
    if not model:
        raise RuntimeError(f"No model configured. Set --model or {configured_name} in .env")
    return model


def discover_candidates(
    *,
    output_dir: Path,
    run_name: str,
    dataset: str,
    model: str,
    split: str,
    selected_problem_keys: set[str] | None = None,
) -> list[Candidate]:
    run_root = output_dir / "direct_generation" / safe_path_component(run_name)
    latest: dict[str, Candidate] = {}
    if not run_root.is_dir():
        return []
    selected_dirs = (
        {safe_path_component(key) for key in selected_problem_keys}
        if selected_problem_keys is not None
        else None
    )
    for metadata_path in run_root.glob(f"*/{dataset}/*/metadata.json"):
        if selected_dirs is not None and metadata_path.parent.name.rsplit("_", 1)[0] not in selected_dirs:
            continue
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        problem = metadata.get("problem", {})
        problem_id = str(problem.get("problem_id", ""))
        artifact_dir = metadata_path.parent
        if (
            metadata.get("requested_model") != model
            or problem.get("dataset") != dataset
            or not problem_id
            or (selected_problem_keys is not None and problem_id not in selected_problem_keys)
            or not is_complete_artifact(metadata, artifact_dir / "solution.py")
        ):
            continue
        candidate = Candidate(
            dataset=dataset,
            problem_id=problem_id,
            split=str(problem.get("split") or split),
            artifact_dir=artifact_dir,
            created_at=str(metadata.get("created_at", "")),
        )
        previous = latest.get(problem_id)
        if previous is None or (candidate.created_at, str(candidate.artifact_dir)) > (
            previous.created_at,
            str(previous.artifact_dir),
        ):
            latest[problem_id] = candidate

    def sort_key(candidate: Candidate) -> tuple[int, str]:
        suffix = candidate.problem_id.removeprefix("HumanEval/")
        return (int(suffix) if suffix.isdigit() else sys.maxsize, candidate.problem_id)

    return sorted(latest.values(), key=sort_key)


def _failure_type(report: dict[str, Any]) -> str:
    if report.get("status") == "passed":
        return "passed"
    statuses = {test.get("status") for test in report.get("tests", [])}
    for status in ("timeout", "runtime_error", "wrong_answer"):
        if status in statuses:
            return status
    return "failed"


def _summary_row(candidate: Candidate, report: dict[str, Any]) -> dict[str, Any]:
    tests = report.get("tests", [])
    status_counts: dict[str, int] = {}
    failed_indices = []
    first_error = report.get("error")
    for test in tests:
        status = str(test.get("status", "unknown"))
        status_counts[status] = status_counts.get(status, 0) + 1
        if not test.get("passed", False):
            failed_indices.append(test.get("index"))
            if first_error is None and test.get("error"):
                first_error = test.get("error")
    return {
        "dataset": candidate.dataset,
        "problem_id": candidate.problem_id,
        "artifact_dir": str(candidate.artifact_dir),
        "status": report.get("status", "failed"),
        "failure_type": _failure_type(report),
        "passed_tests": report.get("passed_tests", 0),
        "total_tests": report.get("total_tests", 0),
        "available_tests": report.get("available_tests", 0),
        "pass_rate": report.get("pass_rate", 0.0),
        "duration_seconds": report.get("duration_seconds", 0.0),
        "failed_test_count": len(failed_indices),
        "failed_test_indices": failed_indices,
        "test_status_counts": status_counts,
        "error": first_error,
    }


def _evaluate_candidate(payload: dict[str, Any]) -> dict[str, Any]:
    candidate = Candidate(
        dataset=payload["dataset"],
        problem_id=payload["problem_id"],
        split=payload["split"],
        artifact_dir=Path(payload["artifact_dir"]),
        created_at=payload["created_at"],
    )
    report_path = Path(payload.get("report_path") or candidate.artifact_dir / "evaluation.json")
    if payload["resume"] and report_path.is_file():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
            return _summary_row(candidate, report)
        except (OSError, json.JSONDecodeError):
            pass

    try:
        solution_path = Path(payload.get("solution_path") or candidate.artifact_dir / "solution.py")
        solution_bytes = solution_path.read_bytes()
        code = solution_bytes.decode("utf-8")
        if candidate.dataset == "apps":
            from Executors import AppsExecutor

            executor = AppsExecutor(
                timeout_per_test=payload["timeout"] or 2.0,
                test_workers=payload["test_workers"],
            )
            test_indices = None
            if payload.get("apps_test_policy") == "private_half":
                test_path = (PROJECT_ROOT / "data" / "apps" / "raw" / candidate.split /
                             f"{int(candidate.problem_id):04d}" / "input_output.json")
                test_data = json.loads(test_path.read_text(encoding="utf-8"))
                total = len(test_data["inputs"])
                if total < 2 or total != len(test_data["outputs"]):
                    raise ValueError(f"Cannot split APPS tests for {candidate.problem_id}")
                test_indices = list(range(total // 2, total))
            execution = executor.evaluate(
                code,
                candidate.problem_id,
                split=candidate.split,
                max_tests=payload["max_tests"],
                test_indices=test_indices,
            )
        else:
            from Executors import HumanevalExecutor

            executor = HumanevalExecutor(timeout=payload["timeout"] or 5.0)
            execution = executor.evaluate(code, candidate.problem_id)
        report = execution.to_dict()
        report["evaluation_provenance"] = {
            "solution_sha256": hashlib.sha256(solution_bytes).hexdigest(),
            "timeout_seconds": payload["timeout"] if payload["timeout"] is not None else (2.0 if candidate.dataset == "apps" else 5.0),
            "test_workers": payload["test_workers"],
            "max_tests": payload["max_tests"],
            "apps_test_policy": payload.get("apps_test_policy", "all"),
            "test_indices": test_indices if candidate.dataset == "apps" else None,
        }
        report_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = report_path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(report_path)
        return _summary_row(candidate, report)
    except Exception as exc:
        return {
            "dataset": candidate.dataset,
            "problem_id": candidate.problem_id,
            "artifact_dir": str(candidate.artifact_dir),
            "status": "executor_error",
            "failure_type": "executor_error",
            "passed_tests": 0,
            "total_tests": 0,
            "available_tests": 0,
            "pass_rate": 0.0,
            "duration_seconds": 0.0,
            "failed_test_count": 0,
            "failed_test_indices": [],
            "test_status_counts": {"executor_error": 1},
            "error": f"{type(exc).__name__}: {exc}",
        }


def _write_aggregate(
    *,
    aggregate_dir: Path,
    rows: list[dict[str, Any]],
    run_name: str,
    model: str,
    dataset: str,
    workers: int,
    evaluation_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    aggregate_dir.mkdir(parents=True, exist_ok=True)
    rows.sort(key=lambda row: row["problem_id"])
    jsonl_path = aggregate_dir / "results.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as output:
        for row in rows:
            output.write(json.dumps(row, ensure_ascii=False) + "\n")
    csv_path = aggregate_dir / "results.csv"
    fields = list(rows[0]) if rows else ["dataset", "problem_id", "status"]
    with csv_path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            csv_row = dict(row)
            for field in ("failed_test_indices", "test_status_counts"):
                if field in csv_row:
                    csv_row[field] = json.dumps(csv_row[field], ensure_ascii=False)
            writer.writerow(csv_row)

    failed_rows = [row for row in rows if row["failure_type"] != "passed"]
    passed_rows = [row for row in rows if row["failure_type"] == "passed"]
    failures_jsonl = aggregate_dir / "failures.jsonl"
    with failures_jsonl.open("w", encoding="utf-8") as output:
        for row in failed_rows:
            output.write(json.dumps(row, ensure_ascii=False) + "\n")
    passed_jsonl = aggregate_dir / "passed.jsonl"
    with passed_jsonl.open("w", encoding="utf-8") as output:
        for row in passed_rows:
            output.write(json.dumps(row, ensure_ascii=False) + "\n")
    failures_csv = aggregate_dir / "failures.csv"
    with failures_csv.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for row in failed_rows:
            csv_row = dict(row)
            for field in ("failed_test_indices", "test_status_counts"):
                if field in csv_row:
                    csv_row[field] = json.dumps(csv_row[field], ensure_ascii=False)
            writer.writerow(csv_row)

    counts: dict[str, int] = {}
    for row in rows:
        failure_type = str(row["failure_type"])
        counts[failure_type] = counts.get(failure_type, 0) + 1
    fully_passed = counts.get("passed", 0)
    total_passed_tests = sum(int(row["passed_tests"]) for row in rows)
    total_tests = sum(int(row["total_tests"]) for row in rows)
    partially_passed = sum(
        0 < int(row["passed_tests"]) < int(row["total_tests"]) for row in rows
    )
    zero_tests_passed = sum(
        int(row["passed_tests"]) == 0 and int(row["total_tests"]) > 0 for row in rows
    )
    summary = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "run_name": run_name,
        "model": model,
        "dataset": dataset,
        "workers": workers,
        "evaluation_config": evaluation_config or {},
        "total_candidates": len(rows),
        "fully_passed": fully_passed,
        "partially_passed": partially_passed,
        "zero_tests_passed": zero_tests_passed,
        "total_passed_tests": total_passed_tests,
        "total_tests": total_tests,
        "pass_at_1": fully_passed / len(rows) if rows else 0.0,
        "micro_test_pass_rate": total_passed_tests / total_tests if total_tests else 0.0,
        "mean_test_pass_rate": statistics.fmean(
            float(row["pass_rate"]) for row in rows
        )
        if rows
        else 0.0,
        "outcomes": counts,
        "failed_problem_ids": [row["problem_id"] for row in failed_rows],
        "results_jsonl": str(jsonl_path),
        "results_csv": str(csv_path),
        "failures_jsonl": str(failures_jsonl),
        "failures_csv": str(failures_csv),
        "passed_jsonl": str(passed_jsonl),
    }
    summary_path = aggregate_dir / "summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    log_path = aggregate_dir / "evaluation.log"
    with log_path.open("w", encoding="utf-8") as output:
        output.write(
            f"run={run_name} dataset={dataset} model={model} workers={workers}\n"
        )
        for row in rows:
            output.write(
                f"problem={row['problem_id']} status={row['failure_type']} "
                f"passed={row['passed_tests']}/{row['total_tests']} "
                f"failed_tests={row['failed_test_indices']} "
                f"artifact={row['artifact_dir']}\n"
            )
            if row.get("error"):
                one_line_error = str(row["error"]).replace("\r", " ").replace("\n", " ")
                output.write(f"  error={one_line_error[:1000]}\n")
        output.write(
            f"summary fully_passed={fully_passed}/{len(rows)} "
            f"partial={partially_passed} zero_passed={zero_tests_passed} "
            f"tests={total_passed_tests}/{total_tests}\n"
        )
    summary["evaluation_log"] = str(log_path)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main(
    argv: list[str] | None = None, *, dataset: str | None = None
) -> int:
    args = parse_args(argv, dataset=dataset)
    model = _target_model(args.model)
    candidates = discover_candidates(
        output_dir=args.output_dir,
        run_name=args.source_run_name or args.run_name,
        dataset=args.dataset,
        model=model,
        split=args.split,
        selected_problem_keys=(
            problem_keys(args.sample_file, dataset=args.dataset)
            if args.sample_file is not None
            else None
        ),
    )
    if args.limit is not None:
        candidates = candidates[: args.limit]
    aggregate_dir = (
        args.output_dir
        / "evaluations"
        / safe_path_component(args.run_name)
        / safe_path_component(model)
        / args.dataset
    )
    config = {
        "source_run_name": args.source_run_name or args.run_name,
        "model": model,
        "dataset": args.dataset,
        "split": args.split,
        "apps_test_policy": args.apps_test_policy,
        "timeout_seconds": args.timeout if args.timeout is not None else (2.0 if args.dataset == "apps" else 5.0),
        "test_workers": args.test_workers,
        "max_tests": args.max_tests,
        "sample_manifest_sha256": hashlib.sha256(args.sample_file.read_bytes()).hexdigest() if args.sample_file else None,
    }
    config_path = aggregate_dir / "evaluation_config.json"
    if config_path.is_file() and json.loads(config_path.read_text(encoding="utf-8")) != config:
        raise SystemExit(f"Evaluation configuration changed; use a new --run-name: {config_path}")
    def report_path(candidate: Candidate) -> Path:
        if args.source_run_name:
            return aggregate_dir / "candidates" / safe_path_component(candidate.problem_id) / "evaluation.json"
        return candidate.artifact_dir / "evaluation.json"

    pending = [candidate for candidate in candidates if args.no_resume or not report_path(candidate).is_file()]
    print(f"Dataset: {args.dataset}")
    print(f"Model: {model}")
    print(f"Source generation run: {config['source_run_name']}")
    print(f"APPS test policy: {args.apps_test_policy}")
    if args.sample_file is not None:
        print(f"Sample file: {args.sample_file}")
    print(f"Discovered candidates: {len(candidates)}")
    print(f"Pending evaluations: {len(pending)}")
    print(f"Workers: {args.workers}")
    print(f"Aggregate output: {aggregate_dir}")
    if args.plan:
        return 0
    if len(candidates) > LARGE_RUN_THRESHOLD and not args.confirm_full_run:
        raise SystemExit(
            f"Refusing to evaluate {len(candidates)} candidates without "
            "--confirm-full-run. Run with --plan first."
        )
    aggregate_dir.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    started_at = datetime.now(timezone.utc)
    started_clock = time.perf_counter()
    payloads = [
        {
            **candidate.__dict__,
            "artifact_dir": str(candidate.artifact_dir),
            "timeout": args.timeout,
            "test_workers": args.test_workers,
            "max_tests": args.max_tests,
            "resume": not args.no_resume,
            "report_path": str(report_path(candidate)),
            "apps_test_policy": args.apps_test_policy,
        }
        for candidate in pending
    ]
    new_rows: list[dict[str, Any]] = []
    failures = 0
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(_evaluate_candidate, payload): payload for payload in payloads}
        for position, future in enumerate(as_completed(futures), start=1):
            row = future.result()
            new_rows.append(row)
            print(
                f"[{position}/{len(payloads)}] {row['problem_id']}: "
                f"{row['passed_tests']}/{row['total_tests']} ({row['failure_type']})",
                flush=True,
            )
            if row["failure_type"] == "executor_error":
                failures += 1
                if args.fail_fast:
                    for outstanding in futures:
                        outstanding.cancel()
                    break

    rows_by_id = {str(row["problem_id"]): row for row in new_rows}
    for candidate in candidates:
        if candidate.problem_id in rows_by_id:
            continue
        path = report_path(candidate)
        if path.is_file():
            try:
                report = json.loads(path.read_text(encoding="utf-8"))
                rows_by_id[candidate.problem_id] = _summary_row(candidate, report)
            except (OSError, json.JSONDecodeError):
                pass
    summary = _write_aggregate(
        aggregate_dir=aggregate_dir,
        rows=list(rows_by_id.values()),
        run_name=args.run_name,
        model=model,
        dataset=args.dataset,
        workers=args.workers,
        evaluation_config={
            "split": args.split,
            "workers": args.workers,
            "test_workers": args.test_workers,
            "timeout_seconds": args.timeout if args.timeout is not None else (2.0 if args.dataset == "apps" else 5.0),
            "timeout_scope": "per_test" if args.dataset == "apps" else "official_harness",
            "test_policy": ("private_second_half" if args.apps_test_policy == "private_half" else "all_input_output_cases") if args.dataset == "apps" else "official_harness",
            "source_run_name": config["source_run_name"],
            "max_tests": args.max_tests,
            "sample_manifest": str(args.sample_file) if args.sample_file is not None else None,
            "sample_manifest_sha256": hashlib.sha256(args.sample_file.read_bytes()).hexdigest() if args.sample_file is not None else None,
        },
    )
    summary["started_at_utc"] = started_at.isoformat()
    summary["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    summary["wall_time_seconds"] = round(time.perf_counter() - started_clock, 3)
    (aggregate_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Evaluation finished: {summary['fully_passed']}/"
        f"{summary['total_candidates']} fully passed"
    )
    return 1 if failures else 0
