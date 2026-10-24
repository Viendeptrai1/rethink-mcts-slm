"""Aggregate the fixed 30-APPS external-evaluator pilot without 300-item finalizers."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from baselines.sample_selection import load_sample_manifest
from evaluation.benchmark_judge import aggregate_group, build_table, DIFFICULTY_ORDER

from .batch import ROOT, _problem_key, _safe_component


APPS_SAMPLE = Path("data/samples/benchmark_v2/apps_test_30_external_evaluator_pilot.json")
HE_SAMPLE = Path("data/samples/benchmark_v2/humaneval_test_164.json")


def _load_result_rows(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not path.is_file():
        raise FileNotFoundError(path)
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            rows[str(row["problem_id"])] = row
    return rows


def _mcts_rows(root: Path, run_name: str, model: str, dataset: str,
               ids: list[int]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    base = root / "outputs/rethinkmcts" / run_name / _safe_component(model) / dataset
    rows: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    for problem_id in ids:
        key = _problem_key(dataset, problem_id)
        problem_dir = base / _safe_component(key)
        summary_path = problem_dir / "search_summary.json"
        if not summary_path.is_file():
            missing.append(key)
            continue
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        report = summary.get("final_evaluation") or summary.get("private_evaluation") or {}
        passed = int(report.get("passed_tests") or 0)
        total = int(report.get("total_tests") or 0)
        if total <= 0 or passed < 0 or passed > total:
            missing.append(key)
            continue
        failure_type = "passed" if passed == total else "failed"
        for test in report.get("tests", []):
            if not test.get("passed") and test.get("status") in {"timeout", "runtime_error", "wrong_answer"}:
                failure_type = test["status"]
                break
        rows[key] = {
            "problem_id": key,
            "passed_tests": passed,
            "total_tests": total,
            "pass_rate": passed / total,
            "failure_type": failure_type,
        }
    return rows, missing


def _metrics(dataset: str, ids: list[int], rows: dict[str, dict[str, Any]], manifest: dict[str, Any]) -> dict[str, Any]:
    groups: dict[str, Any] = {}
    if dataset == "apps":
        difficulty_map = manifest["difficulty_by_problem_id"]
        for group in DIFFICULTY_ORDER:
            selected = [problem_id for problem_id in ids if difficulty_map[str(problem_id)] == group]
            groups[group] = aggregate_group(group=group, problem_ids=selected, rows=rows,
                                            dataset=dataset, difficulty_map=difficulty_map)
        groups["overall"] = aggregate_group(group="overall", problem_ids=ids, rows=rows,
                                            dataset=dataset, difficulty_map=difficulty_map)
    else:
        groups["overall"] = aggregate_group(group="overall", problem_ids=ids, rows=rows, dataset=dataset)
    return {"dataset": dataset, "sample_size": len(ids), "groups": groups}


def _table(apps: dict[str, Any], humaneval: dict[str, Any], method: str) -> dict[str, Any]:
    return build_table(apps=apps, humaneval=humaneval, method=method)


def _write_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = list(rows[0])
    with path.open("w", encoding="utf-8") as output:
        output.write("| " + " | ".join(fields) + " |\n")
        output.write("| " + " | ".join("---" for _ in fields) + " |\n")
        for row in rows:
            output.write("| " + " | ".join(str(row[field]) for field in fields) + " |\n")


def _parse_comparison(value: str) -> tuple[str, Path | None, Path | None]:
    name, separator, paths = value.partition("=")
    if not separator or not name.strip():
        raise argparse.ArgumentTypeError("comparison format is NAME=APPS_RESULTS|HUMANEVAL_RESULTS")
    apps_path, sep, he_path = paths.partition("|")
    if not sep:
        raise argparse.ArgumentTypeError("comparison format is NAME=APPS_RESULTS|HUMANEVAL_RESULTS")
    return name.strip(), Path(apps_path) if apps_path != "-" else None, Path(he_path) if he_path != "-" else None


def build_pilot_report(*, root: Path, run_name: str, model: str, apps_run_name: str,
                       humaneval_run_name: str, apps_sample_file: Path, humaneval_sample_file: Path,
                       comparisons: list[str]) -> Path:
    apps_manifest = load_sample_manifest(apps_sample_file, dataset="apps")
    he_manifest = load_sample_manifest(humaneval_sample_file, dataset="humaneval")
    apps_ids = apps_manifest["problem_ids"]
    he_ids = he_manifest["problem_ids"]
    counts = {name: sum(apps_manifest["difficulty_by_problem_id"][str(pid)] == name for pid in apps_ids)
              for name in DIFFICULTY_ORDER}
    if len(apps_ids) != 30 or counts != {name: 10 for name in DIFFICULTY_ORDER}:
        raise ValueError(f"Pilot APPS manifest must contain 10 IDs per difficulty; got {counts}")
    if len(he_ids) != 164 or set(he_ids) != set(range(164)):
        raise ValueError("Pilot HumanEval manifest must contain all 164 IDs")

    apps_rows, apps_missing = _mcts_rows(root, apps_run_name, model, "apps", apps_ids)
    he_rows, he_missing = _mcts_rows(root, humaneval_run_name, model, "humaneval", he_ids)
    run_config_path = root / "outputs/rethinkmcts" / apps_run_name / _safe_component(model) / "run_config.json"
    run_config = json.loads(run_config_path.read_text(encoding="utf-8")) if run_config_path.is_file() else {}
    evaluator_model = (run_config.get("search") or {}).get("evaluator_model")
    if not evaluator_model:
        raise ValueError("Pilot run_config.json does not identify a separate evaluator model")
    he_config_path = root / "outputs/rethinkmcts" / humaneval_run_name / _safe_component(model) / "run_config.json"
    he_config = json.loads(he_config_path.read_text(encoding="utf-8")) if he_config_path.is_file() else {}
    if not he_config:
        raise FileNotFoundError(he_config_path)

    def search_profile(config: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in config.get("search", {}).items() if key != "run_name"}

    if search_profile(run_config) != search_profile(he_config):
        raise ValueError("APPS and HumanEval pilot search settings differ")
    for field in ("model_digest", "evaluator_model_digest"):
        if (run_config.get("execution") or {}).get(field) != (he_config.get("execution") or {}).get(field):
            raise ValueError(f"APPS and HumanEval {field} differ")
    if run_config.get("model") != model or he_config.get("model") != model:
        raise ValueError("Pilot source run is not from the requested generation model")
    for config in (run_config, he_config):
        for dataset, manifest_path in (("apps", apps_sample_file), ("humaneval", humaneval_sample_file)):
            recorded = (config.get("cohorts") or {}).get(dataset, {})
            digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
            if recorded.get("manifest_sha256") != digest:
                raise ValueError(f"{dataset} manifest differs from the frozen run config")
    methods: list[dict[str, Any]] = []

    def add_method(name: str, apps_data: dict[str, dict[str, Any]], he_data: dict[str, dict[str, Any]] | None) -> None:
        apps_metrics = _metrics("apps", apps_ids, apps_data, apps_manifest)
        if he_data is None:
            he_metrics = {"dataset": "humaneval", "sample_size": None, "available": False,
                          "groups": {"overall": {"pass_at_1_percent": None}}}
        else:
            he_metrics = _metrics("humaneval", he_ids, he_data, he_manifest)
            he_metrics["available"] = True
        methods.append({"method": name, "apps": apps_metrics, "humaneval": he_metrics,
                        "table": _table(apps_metrics, he_metrics, name)})

    add_method("RethinkMCTS Dual (external evaluator)", apps_rows, he_rows)
    comparison_provenance = []
    for value in comparisons:
        name, apps_path, he_path = _parse_comparison(value)
        if apps_path is None:
            raise ValueError(f"Comparison {name!r} must include APPS result JSONL")
        compared_apps = _load_result_rows(apps_path)
        compared_he = _load_result_rows(he_path) if he_path else None
        add_method(name, compared_apps, compared_he)
        comparison_provenance.append({"method": name,
                                      "apps_results": str(apps_path) if apps_path else None,
                                      "humaneval_results": str(he_path) if he_path else None,
                                      "humaneval_available": he_path is not None})

    output = root / "outputs/benchmarks" / run_name / _safe_component(model) / "apps30_pilot"
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite pilot report: {output}")
    output.mkdir(parents=True)
    tables = [item["table"] for item in methods]
    fields = list(tables[0])
    with (output / "benchmark_table.csv").open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(tables)
    _write_markdown(output / "benchmark_table.md", tables)
    summary = {
        "status": "pilot",
        "run_name": run_name,
        "generation_model": model,
        "evaluator_model": evaluator_model,
        "model_digests": {
            "generator": (run_config.get("execution") or {}).get("model_digest"),
            "evaluator": (run_config.get("execution") or {}).get("evaluator_model_digest"),
        },
        "search_config": run_config.get("search"),
        "cohort_provenance": run_config.get("cohorts"),
        "execution_provenance": run_config.get("execution"),
        "cohorts": {"apps": {"manifest": str(apps_sample_file), "sample_size": 30,
                               "difficulty_counts": counts, "missing_candidate_ids": apps_missing},
                    "humaneval": {"manifest": str(humaneval_sample_file), "sample_size": 164,
                                  "missing_candidate_ids": he_missing}},
        "comparison_sources": comparison_provenance,
        "methods": methods,
        "warning": "APPS results are observed on n=30 only; do not label or extrapolate them as n=300.",
        "interpretation_note": "Paired IDs and final-test protocol do not eliminate differences in historical generation provider or prompt version.",
    }
    (output / "benchmark_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "apps_sample_manifest.json").write_bytes(apps_sample_file.read_bytes())
    (output / "humaneval_sample_manifest.json").write_bytes(humaneval_sample_file.read_bytes())
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create an explicitly n=30 APPS pilot report")
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--model", required=True, help="Generation model artifact namespace")
    parser.add_argument("--apps-run-name", help="Defaults to --run-name")
    parser.add_argument("--humaneval-run-name", help="Defaults to --run-name")
    parser.add_argument("--apps-sample-file", type=Path, default=ROOT / APPS_SAMPLE)
    parser.add_argument("--humaneval-sample-file", type=Path, default=ROOT / HE_SAMPLE)
    parser.add_argument("--comparison", action="append", default=[],
                        help="NAME=APPS_RESULTS|HUMANEVAL_RESULTS; use - for unavailable dataset")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    output = build_pilot_report(root=args.root.resolve(), run_name=args.run_name, model=args.model,
                                apps_run_name=args.apps_run_name or args.run_name,
                                humaneval_run_name=args.humaneval_run_name or args.run_name,
                                apps_sample_file=args.apps_sample_file.resolve(),
                                humaneval_sample_file=args.humaneval_sample_file.resolve(),
                                comparisons=args.comparison)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
