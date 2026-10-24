from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from baselines.batch_generation import main as generate_batch
from evaluation.batch_evaluation import main as evaluate_batch
from baselines.direct_generation.pipeline import load_config, safe_path_component


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_ROOT / "baselines" / "direct_generation" / "configs" / "default.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "baselines"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run direct generation first, then parallel evaluation."
    )
    parser.add_argument(
        "--stage", choices=("generate", "evaluate", "all"), default="all"
    )
    parser.add_argument(
        "--dataset", choices=("apps", "humaneval", "all"), default="all"
    )
    parser.add_argument("--run-name", default="direct_full_v1")
    parser.add_argument("--model", default=None)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--sample-file",
        type=Path,
        default=None,
        help="Immutable JSON manifest selecting exact problem IDs for this dataset.",
    )
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--top-p", type=float, default=None)
    parser.add_argument("--reasoning-effort", default=None)
    parser.add_argument("--delay", type=float, default=0.0)
    parser.add_argument("--retries", type=int, default=0)
    parser.add_argument("--generation-workers", type=int, default=2)
    parser.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    parser.add_argument("--test-workers", type=int, default=1)
    parser.add_argument("--evaluation-timeout", type=float, default=None)
    parser.add_argument("--max-tests", type=int, default=None)
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--confirm-full-run", action="store_true")
    args = parser.parse_args(argv)
    if args.limit is not None and args.limit <= 0:
        parser.error("--limit must be greater than zero")
    if args.generation_workers <= 0:
        parser.error("--generation-workers must be greater than zero")
    if args.sample_file is not None:
        args.sample_file = args.sample_file.resolve()
        if args.dataset == "all":
            parser.error(
                "--sample-file belongs to one dataset; run apps and humaneval separately."
            )
    return args


def _shared_args(args: argparse.Namespace) -> list[str]:
    values = [
        "--run-name",
        args.run_name,
        "--output-dir",
        str(args.output_dir.resolve()),
    ]
    if args.model:
        values.extend(("--model", args.model))
    if args.limit is not None:
        values.extend(("--limit", str(args.limit)))
    if args.sample_file is not None:
        values.extend(("--sample-file", str(args.sample_file)))
    if args.no_resume:
        values.append("--no-resume")
    if args.fail_fast:
        values.append("--fail-fast")
    if args.plan:
        values.append("--plan")
    if args.confirm_full_run:
        values.append("--confirm-full-run")
    return values


def _generation_args(args: argparse.Namespace) -> list[str]:
    values = _shared_args(args)
    values.extend(("--config", str(args.config.resolve())))
    for name in ("max_tokens", "temperature", "top_p", "reasoning_effort"):
        value = getattr(args, name)
        if value is not None:
            values.extend((f"--{name.replace('_', '-')}", str(value)))
    if args.delay:
        values.extend(("--delay", str(args.delay)))
    if args.retries:
        values.extend(("--retries", str(args.retries)))
    values.extend(("--generation-workers", str(args.generation_workers)))
    return values


def _evaluation_args(args: argparse.Namespace, dataset: str) -> list[str]:
    values = _shared_args(args)
    values.extend(("--workers", str(args.workers)))
    values.extend(("--test-workers", str(args.test_workers)))
    if args.evaluation_timeout is not None:
        values.extend(("--timeout", str(args.evaluation_timeout)))
    if dataset == "apps" and args.max_tests is not None:
        values.extend(("--max-tests", str(args.max_tests)))
    return values


def _pipeline_log(args: argparse.Namespace, message: str) -> None:
    if args.plan:
        return
    path = (
        args.output_dir.resolve()
        / "pipeline_logs"
        / safe_path_component(args.run_name)
        / safe_path_component(_configured_model(args))
        / "pipeline.log"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as output:
        output.write(f"{datetime.now(timezone.utc).isoformat()} {message}\n")


def _configured_model(args: argparse.Namespace) -> str:
    if args.model:
        return args.model
    try:
        configured = load_config(args.config).model
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        configured = None
    if configured:
        return configured
    return "configured-model"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    datasets = ("apps", "humaneval") if args.dataset == "all" else (args.dataset,)
    _pipeline_log(
        args,
        f"START stage={args.stage} datasets={','.join(datasets)} run={args.run_name}",
    )

    if args.stage in {"generate", "all"}:
        for dataset in datasets:
            print(f"\n=== GENERATE: {dataset} ===")
            _pipeline_log(args, f"GENERATE_START dataset={dataset}")
            status = generate_batch(_generation_args(args), dataset=dataset)
            _pipeline_log(args, f"GENERATE_END dataset={dataset} status={status}")
            if status != 0:
                print(f"Generation failed for {dataset}; evaluation was not started.")
                _pipeline_log(args, f"ABORT generation_failed dataset={dataset}")
                return status

    if args.stage in {"evaluate", "all"}:
        for dataset in datasets:
            print(f"\n=== EVALUATE: {dataset} ===")
            _pipeline_log(args, f"EVALUATE_START dataset={dataset}")
            status = evaluate_batch(_evaluation_args(args, dataset), dataset=dataset)
            _pipeline_log(args, f"EVALUATE_END dataset={dataset} status={status}")
            if status != 0:
                _pipeline_log(args, f"ABORT evaluation_failed dataset={dataset}")
                return status
    _pipeline_log(args, "END status=0")
    return 0
