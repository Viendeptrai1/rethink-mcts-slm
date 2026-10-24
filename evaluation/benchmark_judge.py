from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
from typing import Any, Iterable

from dotenv import load_dotenv

from baselines.sample_selection import load_sample_manifest
from baselines.direct_generation.pipeline import safe_path_component


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "baselines"
DEFAULT_APPS_SAMPLE = PROJECT_ROOT / "data" / "samples" / "benchmark_v2" / "apps_test_300.json"
DEFAULT_HUMANEVAL_SAMPLE = PROJECT_ROOT / "data" / "samples" / "benchmark_v2" / "humaneval_test_164.json"
DIFFICULTY_ORDER = ("introductory", "interview", "competition")
DIFFICULTY_LABELS = {
    "introductory": "APPS Intro.",
    "interview": "APPS Inter.",
    "competition": "APPS Comp.",
}


def target_model(explicit_model: str | None) -> str:
    load_dotenv(PROJECT_ROOT / ".env")
    provider = os.getenv("LLM_PROVIDER", "modal").strip().lower()
    configured_name = "LLM_MODEL" if provider == "ollama" else "KIMI_MODEL"
    model = explicit_model or os.getenv(configured_name)
    if not model:
        raise RuntimeError(f"No model configured. Set --model or {configured_name} in .env")
    return model


def _problem_key(dataset: str, problem_id: int) -> str:
    return f"{problem_id:04d}" if dataset == "apps" else f"HumanEval/{problem_id}"


def _read_results(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not path.is_file():
        return rows
    with path.open("r", encoding="utf-8") as source:
        for line in source:
            if not line.strip():
                continue
            row = json.loads(line)
            rows[str(row["problem_id"])] = row
    return rows


def _normalise_row(problem_id: str, row: dict[str, Any] | None) -> dict[str, Any]:
    if row is None:
        return {
            "problem_id": problem_id,
            "failure_type": "missing_candidate",
            "passed_tests": 0,
            "total_tests": 0,
            "pass_rate": 0.0,
            "missing_candidate": True,
        }
    passed = int(row.get("passed_tests", 0) or 0)
    total = int(row.get("total_tests", 0) or 0)
    return {
        **row,
        "problem_id": problem_id,
        "passed_tests": passed,
        "total_tests": total,
        "pass_rate": float(row.get("pass_rate", 0.0) or 0.0),
        "missing_candidate": False,
    }


def _is_fully_passed(row: dict[str, Any]) -> bool:
    return (
        not row["missing_candidate"]
        and row["total_tests"] > 0
        and row["passed_tests"] == row["total_tests"]
        and row.get("failure_type") == "passed"
    )


def aggregate_group(
    *,
    group: str,
    problem_ids: Iterable[int],
    rows: dict[str, dict[str, Any]],
    dataset: str,
    difficulty_map: dict[str, str] | None = None,
) -> dict[str, Any]:
    selected: list[dict[str, Any]] = []
    for problem_id in problem_ids:
        key = _problem_key(dataset, problem_id)
        selected.append(_normalise_row(key, rows.get(key)))

    expected = len(selected)
    missing_ids = [row["problem_id"] for row in selected if row["missing_candidate"]]
    total_passed_tests = sum(row["passed_tests"] for row in selected)
    total_tests = sum(row["total_tests"] for row in selected)
    fully_passed = sum(_is_fully_passed(row) for row in selected)
    macro_rate = (
        sum(float(row["pass_rate"]) for row in selected) / expected * 100
        if expected
        else 0.0
    )
    micro_rate = total_passed_tests / total_tests * 100 if total_tests else 0.0
    result = {
        "group": group,
        "dataset": dataset,
        "expected_candidates": expected,
        "evaluated_candidates": expected - len(missing_ids),
        "missing_candidates": len(missing_ids),
        "missing_problem_ids": missing_ids,
        "fully_passed": fully_passed,
        "total_passed_tests": total_passed_tests,
        "total_tests": total_tests,
        "pass_at_1_percent": fully_passed / expected * 100 if expected else 0.0,
        "pass_rate_percent": macro_rate if dataset == "apps" else None,
        "micro_pass_rate_percent": micro_rate if dataset == "apps" else None,
    }
    if difficulty_map is not None:
        result["difficulty_counts"] = {
            difficulty: sum(
                difficulty_map[str(problem_id)] == difficulty
                for problem_id in problem_ids
            )
            for difficulty in DIFFICULTY_ORDER
        }
    return result


def build_dataset_metrics(
    *,
    dataset: str,
    sample_path: Path,
    results_path: Path,
    run_name: str,
    model: str,
) -> dict[str, Any]:
    manifest = load_sample_manifest(sample_path, dataset=dataset)
    rows = _read_results(results_path)
    problem_ids = [int(problem_id) for problem_id in manifest["problem_ids"]]
    difficulty_map = manifest.get("difficulty_by_problem_id") if dataset == "apps" else None
    groups: dict[str, dict[str, Any]] = {}
    if dataset == "apps":
        for difficulty in DIFFICULTY_ORDER:
            ids = [
                problem_id
                for problem_id in problem_ids
                if difficulty_map[str(problem_id)] == difficulty
            ]
            groups[difficulty] = aggregate_group(
                group=difficulty,
                problem_ids=ids,
                rows=rows,
                dataset=dataset,
                difficulty_map=difficulty_map,
            )
        groups["overall"] = aggregate_group(
            group="overall",
            problem_ids=problem_ids,
            rows=rows,
            dataset=dataset,
            difficulty_map=difficulty_map,
        )
    else:
        groups["overall"] = aggregate_group(
            group="overall",
            problem_ids=problem_ids,
            rows=rows,
            dataset=dataset,
        )
    return {
        "run_name": run_name,
        "model": model,
        "dataset": dataset,
        "sample_manifest": manifest,
        "results_path": str(results_path),
        "groups": groups,
    }


def _percent(value: float | None) -> str | float:
    return "N/A" if value is None else round(float(value), 2)


def build_table(*, apps: dict[str, Any], humaneval: dict[str, Any], method: str) -> dict[str, Any]:
    row: dict[str, Any] = {"Method": method}
    for difficulty in DIFFICULTY_ORDER:
        label = DIFFICULTY_LABELS[difficulty]
        group = apps["groups"][difficulty]
        row[f"{label} Pass Rate (%)"] = _percent(group["pass_rate_percent"])
        row[f"{label} Pass@1 (%)"] = _percent(group["pass_at_1_percent"])
    overall = apps["groups"]["overall"]
    row["APPS Overall Pass Rate (%)"] = _percent(overall["pass_rate_percent"])
    row["APPS Overall Pass@1 (%)"] = _percent(overall["pass_at_1_percent"])
    row["HumanEval Pass Rate (%)"] = "N/A"
    row["HumanEval Pass@1 (%)"] = _percent(humaneval["groups"]["overall"]["pass_at_1_percent"])
    return row


def _write_markdown(path: Path, row: dict[str, Any]) -> None:
    fields = list(row)
    with path.open("w", encoding="utf-8") as output:
        output.write("| " + " | ".join(fields) + " |\n")
        output.write("| " + " | ".join("---" for _ in fields) + " |\n")
        output.write("| " + " | ".join(str(row[field]) for field in fields) + " |\n")


def write_judge_report(
    *,
    output_dir: Path,
    run_name: str,
    model: str,
    apps_sample_file: Path,
    humaneval_sample_file: Path,
    method: str,
) -> dict[str, Any]:
    base = output_dir / "evaluations" / safe_path_component(run_name) / safe_path_component(model)
    apps = build_dataset_metrics(
        dataset="apps",
        sample_path=apps_sample_file,
        results_path=base / "apps" / "results.jsonl",
        run_name=run_name,
        model=model,
    )
    humaneval = build_dataset_metrics(
        dataset="humaneval",
        sample_path=humaneval_sample_file,
        results_path=base / "humaneval" / "results.jsonl",
        run_name=run_name,
        model=model,
    )
    for metrics in (apps, humaneval):
        dataset_dir = base / metrics["dataset"]
        dataset_dir.mkdir(parents=True, exist_ok=True)
        (dataset_dir / "benchmark_metrics.json").write_text(
            json.dumps(metrics, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    table_row = build_table(apps=apps, humaneval=humaneval, method=method)
    table_csv = base / "benchmark_table.csv"
    with table_csv.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(table_row))
        writer.writeheader()
        writer.writerow(table_row)
    _write_markdown(base / "benchmark_table.md", table_row)
    summary = {
        "run_name": run_name,
        "model": model,
        "method": method,
        "datasets": {"apps": apps, "humaneval": humaneval},
        "table": table_row,
        "benchmark_table_csv": str(table_csv),
        "benchmark_table_md": str(base / "benchmark_table.md"),
    }
    (base / "benchmark_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate sampled benchmark metrics into a paper-style table.")
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--apps-sample-file", type=Path, default=DEFAULT_APPS_SAMPLE)
    parser.add_argument("--humaneval-sample-file", type=Path, default=DEFAULT_HUMANEVAL_SAMPLE)
    parser.add_argument("--method", default="Direct Evaluation")
    parser.add_argument("--plan", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    model = target_model(args.model)
    output_dir = args.output_dir.resolve()
    apps_sample = args.apps_sample_file.resolve()
    humaneval_sample = args.humaneval_sample_file.resolve()
    print(f"Run name: {args.run_name}")
    print(f"Model: {model}")
    print(f"APPS sample: {apps_sample}")
    print(f"HumanEval sample: {humaneval_sample}")
    print(f"Output: {output_dir / 'evaluations' / safe_path_component(args.run_name) / safe_path_component(model)}")
    if args.plan:
        return 0
    summary = write_judge_report(
        output_dir=output_dir,
        run_name=args.run_name,
        model=model,
        apps_sample_file=apps_sample,
        humaneval_sample_file=humaneval_sample,
        method=args.method,
    )
    print(json.dumps(summary["table"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
