from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

from baselines.sample_selection import load_problem_ids
from baselines.direct_generation.pipeline import (
    is_complete_artifact,
    load_config,
    safe_path_component,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_ROOT / "baselines" / "direct_generation" / "configs" / "default.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "baselines"
LARGE_RUN_THRESHOLD = 20


@dataclass(frozen=True)
class GenerationOutcome:
    position: int
    problem_id: int
    result: subprocess.CompletedProcess[str]


def parse_args(
    argv: list[str] | None = None, *, dataset: str
) -> argparse.Namespace:
    maximum_id = 4999 if dataset == "apps" else 163
    default_run = "full_apps_test_v1" if dataset == "apps" else "full_humaneval_v1"
    parser = argparse.ArgumentParser(
        description=f"Generate a resumable {dataset.upper()} batch through Modal."
    )
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=maximum_id)
    parser.add_argument(
        "--limit", type=int, default=None, help="Run only the first N selected IDs."
    )
    parser.add_argument(
        "--sample-file",
        type=Path,
        default=None,
        help="Immutable JSON manifest selecting the exact problem IDs to run.",
    )
    if dataset == "apps":
        parser.add_argument("--split", default="test", choices=("train", "test"))
    else:
        parser.set_defaults(split="test")
    parser.add_argument("--run-name", default=default_run)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--model", default=None)
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--top-p", type=float, default=None)
    parser.add_argument("--reasoning-effort", default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--evaluation-timeout", type=float, default=None)
    if dataset == "apps":
        parser.add_argument("--max-tests", type=int, default=None)
    else:
        parser.set_defaults(max_tests=None)
    parser.add_argument("--delay", type=float, default=0.0, help="Seconds between calls.")
    parser.add_argument(
        "--generation-workers",
        type=int,
        default=2,
        help="Maximum number of concurrent Modal generation requests.",
    )
    parser.add_argument("--retries", type=int, default=0)
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument(
        "--plan", action="store_true", help="Show the resolved batch without calling Modal."
    )
    parser.add_argument(
        "--confirm-full-run",
        action="store_true",
        help=f"Required when more than {LARGE_RUN_THRESHOLD} problems are selected.",
    )
    args = parser.parse_args(argv)

    if args.start < 0 or args.end > maximum_id or args.start > args.end:
        parser.error(f"IDs must satisfy 0 <= start <= end <= {maximum_id}")
    if args.limit is not None and args.limit <= 0:
        parser.error("--limit must be greater than zero")
    if args.delay < 0 or args.retries < 0:
        parser.error("--delay and --retries must not be negative")
    if args.generation_workers <= 0:
        parser.error("--generation-workers must be greater than zero")
    args.config = args.config.resolve()
    args.output_dir = args.output_dir.resolve()
    args.dataset = dataset
    if args.sample_file is not None:
        args.sample_file = args.sample_file.resolve()
    return args


def _selected_ids(args: argparse.Namespace) -> list[int]:
    if args.sample_file is not None:
        problem_ids = load_problem_ids(args.sample_file, dataset=args.dataset)
        problem_ids = [
            problem_id
            for problem_id in problem_ids
            if args.start <= problem_id <= args.end
        ]
    else:
        problem_ids = list(range(args.start, args.end + 1))
    if args.limit is not None:
        problem_ids = problem_ids[: args.limit]
    return problem_ids


def _target_model(args: argparse.Namespace) -> str:
    config = load_config(args.config)
    load_dotenv(PROJECT_ROOT / ".env")
    provider = os.getenv("LLM_PROVIDER", "modal").strip().lower()
    env_model = os.getenv("LLM_MODEL") if provider == "ollama" else os.getenv("KIMI_MODEL")
    model = args.model or config.model or env_model
    if not model:
        env_name = "LLM_MODEL" if provider == "ollama" else "KIMI_MODEL"
        raise RuntimeError(f"No model configured. Set --model or {env_name} in .env")
    return model


def _problem_key(dataset: str, problem_id: int) -> str:
    return f"{problem_id:04d}" if dataset == "apps" else f"HumanEval/{problem_id}"


def _completed_ids(
    args: argparse.Namespace, *, dataset: str, target_model: str
) -> set[str]:
    if args.no_resume:
        return set()
    run_root = args.output_dir / "direct_generation" / safe_path_component(args.run_name)
    if not run_root.is_dir():
        return set()

    completed = set()
    for metadata_path in run_root.glob(f"*/{dataset}/*/metadata.json"):
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        problem = metadata.get("problem", {})
        solution_path = metadata_path.parent / "solution.py"
        response_path = metadata_path.parent / "response.txt"
        evaluation_ready = not args.evaluate or (metadata_path.parent / "evaluation.json").is_file()
        if (
            metadata.get("requested_model") == target_model
            and problem.get("dataset") == dataset
            and is_complete_artifact(metadata, solution_path, response_path)
            and evaluation_ready
        ):
            completed.add(str(problem.get("problem_id")))
    return completed


def _single_command(
    args: argparse.Namespace, *, dataset: str, problem_id: int
) -> list[str]:
    module = "baselines.generate_apps" if dataset == "apps" else "baselines.generate_humaneval"
    command = [
        sys.executable,
        "-m",
        module,
        "--problem-id",
        str(problem_id),
        "--run-name",
        args.run_name,
        "--config",
        str(args.config),
        "--output-dir",
        str(args.output_dir),
        "--quiet",
    ]
    if dataset == "apps":
        command.extend(("--split", args.split))
    for name in ("model", "max_tokens", "temperature", "top_p", "reasoning_effort"):
        value = getattr(args, name)
        if value is not None:
            command.extend((f"--{name.replace('_', '-')}", str(value)))
    if args.evaluate:
        command.append("--evaluate")
        if args.evaluation_timeout is not None:
            command.extend(("--evaluation-timeout", str(args.evaluation_timeout)))
        if dataset == "apps" and args.max_tests is not None:
            command.extend(("--max-tests", str(args.max_tests)))
    return command


def _artifact_from_stdout(stdout: str) -> str | None:
    prefix = "Saved artifact: "
    for line in stdout.splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()
    return None


def _append_manifest(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as manifest:
        manifest.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _append_log(path: Path, message: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    with path.open("a", encoding="utf-8") as output:
        output.write(f"{timestamp} {message}\n")


def _run_problem(
    args: argparse.Namespace,
    *,
    dataset: str,
    position: int,
    problem_id: int,
) -> GenerationOutcome:
    command = _single_command(args, dataset=dataset, problem_id=problem_id)
    result = None
    for attempt in range(args.retries + 1):
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode == 0:
            break
        if attempt < args.retries:
            time.sleep(max(args.delay, 1.0))
    assert result is not None
    return GenerationOutcome(position, problem_id, result)


def main(
    argv: list[str] | None = None, *, dataset: str
) -> int:
    args = parse_args(argv, dataset=dataset)
    problem_ids = _selected_ids(args)
    target_model = _target_model(args)
    completed = _completed_ids(args, dataset=dataset, target_model=target_model)
    pending = [pid for pid in problem_ids if _problem_key(dataset, pid) not in completed]
    manifest_path = (
        args.output_dir
        / "batch_manifests"
        / safe_path_component(args.run_name)
        / safe_path_component(target_model)
        / f"{dataset}.jsonl"
    )
    generation_log = manifest_path.with_name(f"{dataset}.log")

    print(f"Dataset: {dataset}")
    print(f"Split: {args.split}")
    print(f"Model: {target_model}")
    print(f"Run name: {args.run_name}")
    if args.sample_file is not None:
        print(f"Sample file: {args.sample_file}")
    print(f"Selected: {len(problem_ids)}")
    print(f"Already completed: {len(problem_ids) - len(pending)}")
    print(f"Pending: {len(pending)}")
    print(f"Generation workers: {args.generation_workers}")
    print(f"Artifacts: {args.output_dir / 'direct_generation'}")
    print(f"Manifest: {manifest_path}")
    print(f"Generation log: {generation_log}")
    if args.plan:
        return 0
    if len(problem_ids) > LARGE_RUN_THRESHOLD and not args.confirm_full_run:
        raise SystemExit(
            f"Refusing to start {len(problem_ids)} requests without --confirm-full-run. "
            "Run with --plan first."
        )

    failures = 0
    _append_log(
        generation_log,
        f"START run={args.run_name} dataset={dataset} split={args.split} "
        f"model={target_model} selected={len(problem_ids)} pending={len(pending)} "
        f"workers={args.generation_workers}",
    )
    indexed = iter(enumerate(pending, start=1))
    in_flight: dict[Future[GenerationOutcome], tuple[int, int]] = {}
    processed = 0
    stop_submitting = False

    def submit_next(pool: ThreadPoolExecutor) -> bool:
        try:
            position, problem_id = next(indexed)
        except StopIteration:
            return False
        key = _problem_key(dataset, problem_id)
        print(f"[{position}/{len(pending)}] {key}: generating", flush=True)
        future = pool.submit(
            _run_problem,
            args,
            dataset=dataset,
            position=position,
            problem_id=problem_id,
        )
        in_flight[future] = (position, problem_id)
        return True

    with ThreadPoolExecutor(max_workers=args.generation_workers) as pool:
        for _ in range(min(args.generation_workers, len(pending))):
            if in_flight and args.delay:
                time.sleep(args.delay)
            submit_next(pool)

        while in_flight:
            done, _ = wait(in_flight, return_when=FIRST_COMPLETED)
            for future in done:
                in_flight.pop(future)
                outcome = future.result()
                position = outcome.position
                key = _problem_key(dataset, outcome.problem_id)
                result = outcome.result
                artifact = _artifact_from_stdout(result.stdout)
                status = "completed" if result.returncode == 0 else "failed"
                _append_manifest(
                    manifest_path,
                    {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "dataset": dataset,
                        "split": args.split,
                        "problem_id": key,
                        "model": target_model,
                        "status": status,
                        "artifact": artifact,
                        "returncode": result.returncode,
                        "stderr": result.stderr[-4000:] if result.stderr else None,
                    },
                )
                processed += 1
                if result.returncode == 0:
                    print(f"[{position}/{len(pending)}] {key}: saved to {artifact}")
                    _append_log(
                        generation_log,
                        f"problem={key} status=completed artifact={artifact}",
                    )
                else:
                    failures += 1
                    print(f"[{position}/{len(pending)}] {key}: failed", file=sys.stderr)
                    error = (result.stderr or "").replace("\r", " ").replace("\n", " ")
                    _append_log(
                        generation_log,
                        f"problem={key} status=failed returncode={result.returncode} "
                        f"error={error[-1000:]}",
                    )
                    if result.stderr:
                        print(result.stderr[-2000:], file=sys.stderr)
                    if args.fail_fast:
                        stop_submitting = True

            if not stop_submitting:
                for _ in range(len(done)):
                    if args.delay:
                        time.sleep(args.delay)
                    if not submit_next(pool):
                        break

    completed_count = processed - failures
    print(f"Batch finished: {completed_count} completed, {failures} failed")
    _append_log(
        generation_log,
        f"END completed={completed_count} failed={failures} processed={processed}",
    )
    return 1 if failures else 0
