"""Freeze an explicitly adjudicated MCTS table without fabricating candidates."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from baselines.sample_selection import load_sample_manifest
from evaluation.benchmark_judge import build_table
from rethinkmcts.batch import (
    ROOT, SAMPLES, _data_hash, _problem_key, _safe_component, _sha256,
    _source_hash, _validated_summary, validate_cohort,
)
from rethinkmcts.benchmark import _failure_type, _groups, _write_table


RESULT_FIELDS = (
    "dataset", "problem_id", "passed_tests", "total_tests", "pass_rate",
    "failure_type", "adjudicated_failure", "artifact_path", "solution_sha256",
    "best_reward", "request_count",
)


def _read_config(path: Path, *, run_name: str, model: str) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    if config.get("method") != "RethinkMCTS" or config.get("run_name") != run_name or config.get("model") != model:
        raise ValueError(f"Run configuration has a different identity: {path}")
    return config


def _failure_evidence(run_dir: Path, attempt_root: Path, key: str) -> dict[str, Any]:
    progress_path = run_dir / "progress.jsonl"
    attempts = [json.loads(line) for line in progress_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    matching = [row for row in attempts if row.get("dataset") == "apps" and row.get("problem_id") == key]
    if len(matching) < 2 or any(row.get("status") == "completed" for row in matching):
        raise ValueError(f"Adjudication requires at least two failed attempts and no completion: apps/{key}")
    latest = matching[-1]
    if latest.get("status") not in ("failed", "timeout"):
        raise ValueError(f"Latest attempt has no failure status: apps/{key}")
    attempt_dir = Path(str(latest.get("attempt_dir") or "")).resolve()
    if attempt_dir.parent != (attempt_root / "apps" / key).resolve():
        raise ValueError(f"Attempt path escapes expected run directory: apps/{key}")
    log = attempt_dir / "attempt.log"
    if not log.is_file():
        raise FileNotFoundError(log)
    return {
        "problem_id": key,
        "attempt_count": len(matching),
        "latest_status": latest["status"],
        "latest_error": latest.get("error"),
        "latest_attempt_log": str(log),
        "latest_attempt_log_sha256": _sha256(log),
    }


def finalize_adjudicated(
    *, root: Path, run_name: str, model: str, humaneval_run_name: str,
    failed_apps: list[str],
) -> Path:
    root = root.resolve()
    if any(_safe_component(value) != value for value in (run_name, humaneval_run_name)):
        raise ValueError("Unsafe run name")
    failed = set(failed_apps)
    if len(failed) != len(failed_apps) or not failed:
        raise ValueError("Pass unique, nonempty --failed-apps IDs")
    model_dir = _safe_component(model)
    apps_dir = root / "outputs/rethinkmcts" / run_name / model_dir
    humaneval_dir = root / "outputs/rethinkmcts" / humaneval_run_name / model_dir
    apps_config_path = apps_dir / "run_config.json"
    humaneval_config_path = humaneval_dir / "run_config.json"
    apps_config = _read_config(apps_config_path, run_name=run_name, model=model)
    humaneval_config = _read_config(humaneval_config_path, run_name=humaneval_run_name, model=model)
    if apps_config["execution"]["source_sha256"] != _source_hash(root):
        raise ValueError("Search source changed since the APPS run started")
    for field in ("provider", "model_digest"):
        if not apps_config["execution"].get(field) or apps_config["execution"][field] != humaneval_config["execution"].get(field):
            raise ValueError(f"Run {field} values are missing or differ")
    apps_search = {key: value for key, value in apps_config["search"].items() if key != "run_name"}
    humaneval_search = {key: value for key, value in humaneval_config["search"].items() if key != "run_name"}
    if apps_search != humaneval_search:
        raise ValueError("Search settings differ between source runs")

    manifests = {name: load_sample_manifest(root / path, dataset=name) for name, path in SAMPLES.items()}
    validate_cohort(manifests)
    apps_ids = {_problem_key("apps", problem_id) for problem_id in manifests["apps"]["problem_ids"]}
    if not failed <= apps_ids:
        raise ValueError("Failed APPS IDs must belong to the locked cohort")

    evidence: dict[str, str] = {
        "apps_run_config": _sha256(apps_config_path),
        "humaneval_run_config": _sha256(humaneval_config_path),
        "apps_progress": _sha256(apps_dir / "progress.jsonl"),
    }
    failure_details: list[dict[str, Any]] = []
    attempt_root = root / "outputs/rethinkmcts_attempts" / run_name / model_dir
    for key in sorted(failed):
        detail = _failure_evidence(apps_dir, attempt_root, key)
        failure_details.append(detail)
        evidence[f"apps/{key}/failed_attempt"] = detail["latest_attempt_log_sha256"]

    datasets: dict[str, dict[str, Any]] = {}
    results: dict[str, list[dict[str, Any]]] = {}
    candidate_index: list[dict[str, Any]] = []
    for dataset in SAMPLES:
        config = apps_config if dataset == "apps" else humaneval_config
        source_dir = apps_dir if dataset == "apps" else humaneval_dir
        manifest = manifests[dataset]
        ids = manifest["problem_ids"]
        cohort = config["cohorts"][dataset]
        if cohort["manifest_sha256"] != _sha256(root / SAMPLES[dataset]) or cohort["test_data_sha256"] != _data_hash(root, dataset, ids):
            raise ValueError(f"{dataset} manifest or data changed")
        metric_rows: dict[str, dict[str, Any]] = {}
        dataset_results: list[dict[str, Any]] = []
        for problem_id in ids:
            key = _problem_key(dataset, problem_id)
            artifact = source_dir / dataset / _safe_component(key)
            summary = _validated_summary(artifact, config, dataset, key)
            if dataset == "apps" and key in failed:
                if summary is not None or artifact.exists():
                    raise ValueError(f"Cannot adjudicate an existing artifact: apps/{key}")
                row = {
                    "dataset": dataset, "problem_id": key, "passed_tests": 0,
                    "total_tests": 0, "pass_rate": 0.0,
                    "failure_type": next(detail["latest_status"] for detail in failure_details if detail["problem_id"] == key),
                    "adjudicated_failure": True, "artifact_path": None,
                    "solution_sha256": None, "best_reward": None, "request_count": None,
                }
                dataset_results.append(row)
                candidate_index.append(row)
                continue
            if summary is None:
                raise ValueError(f"Incomplete cohort without adjudication: {dataset}/{key}")
            report = summary.get("final_evaluation") or summary.get("private_evaluation") or {}
            passed = int(report.get("passed_tests") or 0)
            total = int(report.get("total_tests") or 0)
            if total <= 0 or passed < 0 or passed > total or report.get("status") not in ("passed", "failed"):
                raise ValueError(f"Invalid private evaluation: {dataset}/{key}")
            solution_hash = _sha256(artifact / "final_solution.py")
            row = {
                "dataset": dataset, "problem_id": key, "passed_tests": passed,
                "total_tests": total, "pass_rate": passed / total,
                "failure_type": _failure_type(report), "adjudicated_failure": False,
                "artifact_path": artifact.relative_to(root).as_posix(),
                "solution_sha256": solution_hash, "best_reward": summary.get("best_reward"),
                "request_count": summary.get("request_count"),
            }
            metric_rows[key] = row
            dataset_results.append(row)
            candidate_index.append(row)
            evidence[f"{dataset}/{key}/summary"] = _sha256(artifact / "search_summary.json")
            evidence[f"{dataset}/{key}/solution"] = solution_hash
        groups = _groups(dataset, ids, metric_rows, manifest)
        datasets[dataset] = {
            "dataset": dataset, "sample_manifest": manifest, "groups": groups,
            "test_policy": "apps_private_second_half" if dataset == "apps" else "official_harness",
            "adjudicated_failures": failure_details if dataset == "apps" else [],
        }
        results[dataset] = dataset_results

    table = build_table(apps=datasets["apps"], humaneval=datasets["humaneval"], method="RethinkMCTS (adjudicated)")
    fingerprint = hashlib.sha256(json.dumps(evidence, sort_keys=True).encode("utf-8")).hexdigest()
    target = root / "outputs/benchmarks" / run_name / model_dir / "adjudicated_v1"
    if target.exists():
        prior = json.loads((target / "run.json").read_text(encoding="utf-8"))
        if prior.get("source_fingerprint") == fingerprint:
            return target
        raise FileExistsError(f"Refusing to replace a different adjudicated report: {target}")
    record = {
        "schema_version": 1, "status": "adjudicated_complete",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_name": run_name, "model": model,
        "model_revision": apps_config["execution"]["model_digest"],
        "method": "RethinkMCTS (adjudicated)",
        "source_runs": {"apps": run_name, "humaneval": humaneval_run_name},
        "source_code_sha256_by_dataset": {
            "apps": apps_config["execution"]["source_sha256"],
            "humaneval": humaneval_config["execution"]["source_sha256"],
        },
        "search_profile": apps_search,
        "adjudication_policy": "Listed missing APPS candidates count as zero for macro Pass Rate and Pass@1; no private tests are claimed to have run.",
        "coverage": {
            "apps": {"expected": 300, "completed": 300 - len(failed), "adjudicated_failure": len(failed)},
            "humaneval": {"expected": 164, "completed": 164, "adjudicated_failure": 0},
        },
        "adjudicated_failures": failure_details,
        "metrics": table, "source_hashes": evidence, "source_fingerprint": fingerprint,
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".adjudicated-", dir=target.parent))
    try:
        (staging / "run.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (staging / "benchmark_summary.json").write_text(json.dumps({
            "run_name": run_name, "model": model, "method": record["method"],
            "datasets": datasets, "table": table, "coverage": record["coverage"],
            "adjudication_policy": record["adjudication_policy"],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _write_table(staging / "benchmark_table.md", table)
        with (staging / "benchmark_table.csv").open("w", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=list(table))
            writer.writeheader()
            writer.writerow(table)
        with (staging / "candidates.csv").open("w", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=RESULT_FIELDS)
            writer.writeheader()
            writer.writerows(candidate_index)
        for dataset, rows in results.items():
            folder = staging / dataset
            folder.mkdir()
            shutil.copy2(root / SAMPLES[dataset], folder / "sample_manifest.json")
            with (folder / "results.jsonl").open("w", encoding="utf-8") as output:
                for row in rows:
                    output.write(json.dumps(row, ensure_ascii=False) + "\n")
            with (folder / "results.csv").open("w", encoding="utf-8", newline="") as output:
                writer = csv.DictWriter(output, fieldnames=RESULT_FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            (folder / "benchmark_metrics.json").write_text(json.dumps(datasets[dataset], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        staging.rename(target)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report explicit missing APPS searches as adjudicated failures")
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--humaneval-run-name", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--failed-apps", nargs="+", required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    print(finalize_adjudicated(root=args.root, run_name=args.run_name, model=args.model,
                               humaneval_run_name=args.humaneval_run_name, failed_apps=args.failed_apps))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
