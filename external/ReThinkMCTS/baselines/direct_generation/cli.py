from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, replace
from datetime import datetime, timezone
from pathlib import Path

from ChatModels import ModalClient, OllamaClient
from DataProcess import load_problem

from .pipeline import build_user_prompt, extract_code, load_config, save_artifact


PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = PACKAGE_DIR / "configs" / "default.json"
DEFAULT_OUTPUT_DIR = PACKAGE_DIR.parents[1] / "outputs" / "baselines"


def parse_args(
    argv: list[str] | None = None, *, dataset: str | None = None
) -> argparse.Namespace:
    description = "Generate one direct solution with the configured LLM provider."
    if dataset:
        description = f"Generate one direct solution for {dataset.upper()}."
    parser = argparse.ArgumentParser(
        description=description
    )
    if dataset is None:
        parser.add_argument("--dataset", required=True, choices=("apps", "humaneval"))
    else:
        parser.set_defaults(dataset=dataset)
    parser.add_argument("--problem-id", required=True)
    if dataset != "humaneval":
        parser.add_argument("--split", default="test", choices=("train", "test"))
    else:
        parser.set_defaults(split="test")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-name", default=None)
    parser.add_argument("--model", default=None, help="Override the configured model for this run.")
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--top-p", type=float, default=None)
    parser.add_argument("--reasoning-effort", default=None)
    parser.add_argument(
        "--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the resolved config and prompt without calling Modal.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Do not print generated source code; keep artifact summaries.",
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Run dataset tests and save evaluation.json after generation.",
    )
    parser.add_argument(
        "--evaluation-timeout",
        type=float,
        default=None,
        help="Per-test APPS timeout or whole-harness HumanEval timeout.",
    )
    parser.add_argument(
        "--evaluation-test-workers",
        type=int,
        default=1,
        help="APPS tests to execute concurrently when --evaluate is enabled.",
    )
    if dataset != "humaneval":
        parser.add_argument(
            "--max-tests",
            type=int,
            default=None,
            help="Evaluate only the first N APPS tests.",
        )
    else:
        parser.set_defaults(max_tests=None)
    return parser.parse_args(argv)


def _resolve_config(args: argparse.Namespace):
    config = load_config(args.config)
    overrides = {
        "run_name": args.run_name,
        "model": args.model,
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "reasoning_effort": args.reasoning_effort,
    }
    config = replace(
        config,
        **{name: value for name, value in overrides.items() if value is not None},
    )
    config.validate()
    return config


def _build_client():
    provider = os.getenv("LLM_PROVIDER", "modal").strip().lower()
    if provider == "ollama":
        return OllamaClient()
    if provider == "modal":
        return ModalClient()
    raise ValueError(f"Unsupported LLM_PROVIDER: {provider}. Use ollama or modal.")


def _evaluate_artifact(args: argparse.Namespace, code: str, run_dir: Path):
    if args.dataset == "apps":
        from Executors import AppsExecutor

        timeout = args.evaluation_timeout if args.evaluation_timeout is not None else 2.0
        executor = AppsExecutor(
            timeout_per_test=timeout,
            test_workers=getattr(args, "evaluation_test_workers", 1),
        )
        report = executor.evaluate(
            code,
            args.problem_id,
            split=args.split,
            max_tests=args.max_tests,
        )
    else:
        if args.max_tests is not None:
            raise ValueError("--max-tests only applies to APPS")
        from Executors import HumanevalExecutor

        timeout = args.evaluation_timeout if args.evaluation_timeout is not None else 5.0
        executor = HumanevalExecutor(timeout=timeout)
        report = executor.evaluate(code, args.problem_id)

    report_path = run_dir / "evaluation.json"
    report_path.write_text(report.to_json() + "\n", encoding="utf-8")
    return report, report_path


def main(
    argv: list[str] | None = None, *, dataset: str | None = None
) -> int:
    args = parse_args(argv, dataset=dataset)
    config = _resolve_config(args)
    problem = load_problem(args.dataset, args.problem_id, split=args.split)
    user_prompt = build_user_prompt(problem)

    if args.dry_run:
        provider = os.getenv("LLM_PROVIDER", "modal").strip().lower()
        model_env = "LLM_MODEL" if provider == "ollama" else "KIMI_MODEL"
        print(f"Config: {args.config}")
        print(f"Run name: {config.run_name}")
        print(f"Provider: {provider}")
        print(f"Selected model: {config.model or f'<from {model_env}>'}")
        print(f"Generation: {asdict(config)}")
        print("\n--- Prompt ---\n")
        print(user_prompt)
        return 0

    client = _build_client()
    selected_model = config.model or client.model
    result = client.generate(
        [
            {"role": "system", "content": config.system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model=selected_model,
        max_tokens=config.max_tokens,
        temperature=config.temperature,
        top_p=config.top_p,
        reasoning_effort=config.reasoning_effort,
    )
    code = extract_code(result.content)
    generation_complete = bool(code.strip()) and result.finish_reason in (None, "stop")
    if not code.strip():
        generation_issue = "empty_solution"
    elif result.finish_reason not in (None, "stop"):
        generation_issue = f"incomplete_finish_reason:{result.finish_reason}"
    else:
        generation_issue = None
    metadata = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "baseline": "direct_generation",
        "run_name": config.run_name,
        "config_file": str(args.config),
        "problem": {
            "dataset": problem.dataset,
            "problem_id": problem.problem_id,
            "split": args.split,
            "entry_point": problem.entry_point,
            "statement": "stored in problem.txt",
        },
        "requested_model": selected_model,
        "response_model": result.model,
        "finish_reason": result.finish_reason,
        "generation_complete": generation_complete,
        "generation_issue": generation_issue,
        "usage": result.usage,
        "generation": asdict(config),
        "evaluation": None,
    }
    run_dir = save_artifact(
        args.output_dir,
        run_name=config.run_name,
        model=selected_model,
        problem=problem,
        user_prompt=user_prompt,
        raw_response=result.content,
        code=code,
        metadata=metadata,
    )

    if not args.quiet:
        print(code)
    print(f"\nSaved artifact: {run_dir}")
    if not generation_complete:
        print(
            f"Incomplete generation: {generation_issue}. This problem remains pending.",
            file=sys.stderr,
        )
        return 2
    if args.evaluate:
        report, report_path = _evaluate_artifact(args, code, run_dir)
        metadata["evaluation"] = {
            "report_file": report_path.name,
            "status": report.status,
            "passed_tests": report.passed_tests,
            "total_tests": report.total_tests,
            "available_tests": report.available_tests,
            "pass_rate": report.pass_rate,
        }
        (run_dir / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(
            "Evaluation: "
            f"{report.passed_tests}/{report.total_tests} passed "
            f"({report.pass_rate:.2%})"
        )
        print(f"Saved evaluation: {report_path}")
    else:
        command = (
            f'& "{Path(sys.executable)}" -m Executors '
            f'--dataset {args.dataset} --problem-id "{args.problem_id}" '
            f'--code-file "{run_dir / "solution.py"}" '
            f'--report-file "{run_dir / "evaluation.json"}"'
        )
        if args.dataset == "apps":
            command += f" --split {args.split}"
        print("Evaluate later: " + command)
    return 0
