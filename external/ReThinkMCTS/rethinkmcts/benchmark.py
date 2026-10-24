from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from baselines.sample_selection import load_sample_manifest
from evaluation.benchmark_judge import DIFFICULTY_ORDER, aggregate_group, build_table

from .batch import ROOT, SAMPLES, _data_hash, _problem_key, _safe_component, _sha256, _source_hash, _validated_summary, validate_cohort


INDEX_FIELDS = (
    "dataset", "problem_id", "artifact_path", "solution_sha256", "best_candidate_id",
    "best_reward", "request_count", "prompt_tokens", "completion_tokens", "total_tokens",
    "passed_tests", "total_tests", "failure_type",
)
RESULT_FIELDS = (
    "dataset", "problem_id", "passed_tests", "total_tests", "pass_rate", "failure_type",
    "best_reward", "request_count", "solution_sha256",
)


def _failure_type(report: dict[str, Any]) -> str:
    if report.get("status") == "passed" and report.get("passed_tests") == report.get("total_tests"):
        return "passed"
    statuses = {str(test.get("status")) for test in report.get("tests", [])}
    for status in ("timeout", "runtime_error", "wrong_answer"):
        if status in statuses:
            return status
    return "failed"


def _write_table(path: Path, row: dict[str, Any]) -> None:
    fields = list(row)
    with path.open("w", encoding="utf-8") as output:
        output.write("| " + " | ".join(fields) + " |\n")
        output.write("| " + " | ".join("---" for _ in fields) + " |\n")
        output.write("| " + " | ".join(str(row[field]) for field in fields) + " |\n")


def _groups(dataset: str, ids: list[int], rows: dict[str, dict[str, Any]], manifest: dict[str, Any]) -> dict[str, Any]:
    if dataset == "humaneval":
        return {"overall": aggregate_group(group="overall", problem_ids=ids, rows=rows, dataset=dataset)}
    difficulty_map = manifest["difficulty_by_problem_id"]
    groups = {
        difficulty: aggregate_group(
            group=difficulty,
            problem_ids=[problem_id for problem_id in ids if difficulty_map[str(problem_id)] == difficulty],
            rows=rows, dataset=dataset, difficulty_map=difficulty_map,
        )
        for difficulty in DIFFICULTY_ORDER
    }
    groups["overall"] = aggregate_group(
        group="overall", problem_ids=ids, rows=rows, dataset=dataset, difficulty_map=difficulty_map,
    )
    return groups


def finalize_benchmark(*, root: Path, run_name: str, model: str, humaneval_run_name: str | None = None) -> Path:
    root = root.resolve()
    if _safe_component(run_name) != run_name:
        raise ValueError("Unsafe run name")
    model_dir = _safe_component(model)
    run_dir = root / "outputs/rethinkmcts" / run_name / model_dir
    config = json.loads((run_dir / "run_config.json").read_text(encoding="utf-8"))
    if config.get("method") != "RethinkMCTS" or config.get("run_name") != run_name or config.get("model") != model:
        raise ValueError("Run configuration belongs to another experiment")
    if config["execution"]["source_sha256"] != _source_hash(root):
        raise ValueError("Source code changed since the MCTS batch was started")
    humaneval_run_name = humaneval_run_name or run_name
    if _safe_component(humaneval_run_name) != humaneval_run_name:
        raise ValueError("Unsafe HumanEval run name")
    humaneval_run_dir = root / "outputs/rethinkmcts" / humaneval_run_name / model_dir
    humaneval_config_path = humaneval_run_dir / "run_config.json"
    humaneval_config = json.loads(humaneval_config_path.read_text(encoding="utf-8"))
    if humaneval_config.get("method") != "RethinkMCTS" or humaneval_config.get("run_name") != humaneval_run_name or humaneval_config.get("model") != model:
        raise ValueError("HumanEval source belongs to another experiment")
    if humaneval_run_name != run_name:
        def search_profile(value: dict[str, Any]) -> dict[str, Any]:
            return {key: item for key, item in value["search"].items() if key != "run_name"}

        if search_profile(config) != search_profile(humaneval_config):
            raise ValueError("APPS and HumanEval search settings differ")
        for field in ("provider", "model_digest"):
            if config["execution"].get(field) != humaneval_config["execution"].get(field):
                raise ValueError(f"APPS and HumanEval {field} differ")
        if not config["execution"].get("model_digest"):
            raise ValueError("Cross-run benchmark requires a pinned model digest")
    datasets: dict[str, Any] = {}
    results_by_dataset: dict[str, list[dict[str, Any]]] = {}
    candidates: list[dict[str, Any]] = []
    evidence: dict[str, str] = {
        "run_config": _sha256(run_dir / "run_config.json"),
        "humaneval_run_config": _sha256(humaneval_config_path),
    }
    cohorts: dict[str, Any] = {}
    manifests = {dataset: load_sample_manifest(root / sample, dataset=dataset) for dataset, sample in SAMPLES.items()}
    validate_cohort(manifests)
    for dataset, sample in SAMPLES.items():
        source_dir = humaneval_run_dir if dataset == "humaneval" else run_dir
        source_config = humaneval_config if dataset == "humaneval" else config
        sample_path = root / sample
        manifest = manifests[dataset]
        ids = manifest["problem_ids"]
        config_cohort = config["cohorts"][dataset]
        if config_cohort["manifest_sha256"] != _sha256(sample_path) or config_cohort["test_data_sha256"] != _data_hash(root, dataset, ids):
            raise ValueError(f"{dataset} manifest or data changed since batch start")
        if source_config["cohorts"][dataset] != config_cohort:
            raise ValueError(f"{dataset} source cohort differs from destination run")
        rows: dict[str, dict[str, Any]] = {}
        index_rows: list[dict[str, Any]] = []
        test_policy = "official_harness" if dataset == "humaneval" else None
        for problem_id in ids:
            key = _problem_key(dataset, problem_id)
            artifact = source_dir / dataset / _safe_component(key)
            summary = _validated_summary(artifact, source_config, dataset, key)
            if summary is None:
                raise ValueError(f"Incomplete MCTS cohort: missing {dataset}/{key}")
            report = summary.get("final_evaluation") or summary.get("private_evaluation") or {}
            if dataset == "apps":
                current_policy = "all_input_output_cases" if summary.get("final_evaluation") else "apps_private_second_half"
                if test_policy is not None and test_policy != current_policy:
                    raise ValueError("Mixed APPS final-evaluation policies in one run")
                test_policy = current_policy
            passed = int(report.get("passed_tests") or 0)
            total = int(report.get("total_tests") or 0)
            if total <= 0 or passed < 0 or passed > total or report.get("status") not in ("passed", "failed"):
                raise ValueError(f"Invalid private evaluation for {dataset}/{key}")
            solution_hash = _sha256(artifact / "final_solution.py")
            usage = summary.get("token_usage") or {}
            failure_type = _failure_type(report)
            row = {
                "dataset": dataset, "problem_id": key, "passed_tests": passed,
                "total_tests": total, "pass_rate": passed / total,
                "failure_type": failure_type, "best_reward": summary.get("best_reward"),
                "request_count": summary.get("request_count"), "solution_sha256": solution_hash,
            }
            rows[key] = row
            index_rows.append({
                "dataset": dataset, "problem_id": key,
                "artifact_path": artifact.relative_to(root).as_posix(),
                "solution_sha256": solution_hash,
                "best_candidate_id": summary.get("best_candidate_id"),
                "best_reward": summary.get("best_reward"),
                "request_count": summary.get("request_count"),
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
                "passed_tests": passed, "total_tests": total, "failure_type": failure_type,
            })
            evidence[f"{dataset}/{key}/summary"] = _sha256(artifact / "search_summary.json")
            evidence[f"{dataset}/{key}/solution"] = solution_hash
        groups = _groups(dataset, ids, rows, manifest)
        datasets[dataset] = {
            "dataset": dataset, "sample_manifest": manifest,
            "groups": groups,
            "test_policy": test_policy,
        }
        results_by_dataset[dataset] = [rows[_problem_key(dataset, value)] for value in ids]
        candidates.extend(index_rows)
        cohorts[dataset] = {
            **config_cohort,
            "manifest": sample.as_posix(),
            "difficulty_counts": groups["overall"].get("difficulty_counts"),
        }
    table = build_table(apps=datasets["apps"], humaneval=datasets["humaneval"], method="RethinkMCTS")
    fingerprint = hashlib.sha256(json.dumps(evidence, sort_keys=True).encode("utf-8")).hexdigest()
    target = root / "outputs/benchmarks" / run_name / model_dir
    if target.exists():
        previous = json.loads((target / "run.json").read_text(encoding="utf-8"))
        if previous.get("source_fingerprint") == fingerprint:
            return target
        raise FileExistsError(f"Frozen benchmark has different inputs: {target}")
    record = {
        "schema_version": 1, "status": "complete", "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_name": run_name, "model": model, "model_revision": config["execution"].get("model_digest"),
        "method": "RethinkMCTS", "provider": "ollama", "source_generation_run": None,
        "cohorts": cohorts, "generation_profiles": [config["search"]],
        "source_runs": {"apps": run_name, "humaneval": humaneval_run_name},
        "evaluation": {
            dataset: {
                "split": "test", "workers": (humaneval_config if dataset == "humaneval" else config)["batch"].get("workers", 1), "test_workers": 1,
                "timeout_seconds": config["search"]["timeout_seconds"],
                "timeout_scope": "per_test" if dataset == "apps" else "official_harness",
                "test_policy": datasets[dataset]["test_policy"], "max_tests": None,
            }
            for dataset in SAMPLES
        },
        "coverage": {dataset: {"expected": len(results), "evaluated": len(results), "missing": 0, "executor_errors": 0}
                     for dataset, results in results_by_dataset.items()},
        "execution": {
            "site": "local_judge_modal_gpu_inference" if config["execution"].get("provider") == "modal_gpu" else "ckey_gpu",
            "backend": "modal_gpu" if config["execution"].get("provider") == "modal_gpu" else "docker" if config["execution"].get("image_id") else "local",
            "image_id": config["execution"].get("image_id"),
            "python_version": config["execution"]["python_version"],
            "platform": platform.platform(), "code_sha256": config["execution"]["source_sha256"],
            "source_code_sha256_by_dataset": {
                "apps": config["execution"]["source_sha256"],
                "humaneval": humaneval_config["execution"]["source_sha256"],
            },
            "modal_inference_sha256_by_dataset": {
                "apps": config["execution"].get("modal_inference_sha256"),
                "humaneval": humaneval_config["execution"].get("modal_inference_sha256"),
            },
            "gpu_type_by_dataset": {
                "apps": config["execution"].get("gpu_type"),
                "humaneval": humaneval_config["execution"].get("gpu_type"),
            },
            "problem_timeout_seconds": config["batch"]["problem_timeout_seconds"],
        },
        "metrics": table, "source_hashes": evidence, "source_fingerprint": fingerprint,
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{model_dir}.", dir=target.parent))
    try:
        (staging / "run.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        with (staging / "candidates.csv").open("w", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=INDEX_FIELDS)
            writer.writeheader()
            writer.writerows(candidates)
        with (staging / "benchmark_table.csv").open("w", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=list(table))
            writer.writeheader()
            writer.writerow(table)
        _write_table(staging / "benchmark_table.md", table)
        (staging / "benchmark_summary.json").write_text(json.dumps({
            "run_name": run_name, "model": model, "method": "RethinkMCTS",
            "datasets": datasets, "table": table,
            "request_count": sum(int(row.get("request_count") or 0) for row in candidates),
            "total_tokens": sum(int(row.get("total_tokens") or 0) for row in candidates),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for dataset, rows in results_by_dataset.items():
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
    parser = argparse.ArgumentParser(description="Freeze a complete 300+164 RethinkMCTS benchmark")
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--humaneval-run-name", help="Reuse a complete HumanEval run with the same model and search protocol")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    print(finalize_benchmark(root=args.root, run_name=args.run_name, model=args.model,
                             humaneval_run_name=args.humaneval_run_name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
