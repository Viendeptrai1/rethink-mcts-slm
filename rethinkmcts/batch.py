from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import signal
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from baselines.sample_selection import load_sample_manifest

from .config import SearchConfig


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = {
    "apps": Path("data/samples/benchmark_v2/apps_test_300.json"),
    "humaneval": Path("data/samples/benchmark_v2/humaneval_test_164.json"),
}


def validate_cohort(manifests: dict[str, dict[str, Any]]) -> None:
    ids = manifests["apps"]["problem_ids"]
    difficulties = manifests["apps"]["difficulty_by_problem_id"]
    counts = {name: sum(difficulties[str(problem_id)] == name for problem_id in ids)
              for name in ("introductory", "interview", "competition")}
    if len(ids) == 300 and counts == {name: 100 for name in counts}:
        pass
    elif (len(ids) == 30 and counts == {name: 10 for name in counts}
          and str(manifests["apps"].get("sample_id", "")).startswith("apps_pilot_30_")):
        pass
    else:
        raise ValueError(f"APPS cohort must be benchmark_v2 (300, 100/difficulty) or a locked 30-item pilot (10/difficulty); got {len(ids)} and {counts}")
    if len(manifests["humaneval"]["problem_ids"]) != 164:
        raise ValueError("HumanEval cohort must contain all 164 problems")


def _sample_paths(args: argparse.Namespace) -> dict[str, Path]:
    apps_path = args.apps_sample_file
    if not apps_path.is_absolute():
        apps_path = ROOT / apps_path
    return {"apps": apps_path.resolve(), "humaneval": ROOT / SAMPLES["humaneval"]}


def _safe_component(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._") or "unnamed"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _files_hash(root: Path, files: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(files):
        if not path.is_file():
            raise FileNotFoundError(path)
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _source_hash(root: Path) -> str:
    files = [
        path for directory in ("rethinkmcts", "ChatModels", "DataProcess", "Executors")
        for path in (root / directory).rglob("*.py")
    ]
    files.append(root / "baselines/sample_selection.py")
    files.append(root / "evaluation/benchmark_judge.py")
    return _files_hash(root, files)


def _data_hash(root: Path, dataset: str, ids: list[int]) -> str:
    if dataset == "apps":
        files = []
        for problem_id in ids:
            problem_dir = root / "data/apps/raw/test" / f"{problem_id:04d}"
            files.extend((problem_dir / name for name in ("question.txt", "input_output.json")))
            starter = problem_dir / "starter_code.py"
            if starter.is_file():
                files.append(starter)
    else:
        files = [path for path in (root / "data/humaneval/arrow").rglob("*") if path.is_file()]
        files.extend((root / "data/humaneval/public_tests.jsonl", root / "data/humaneval/public_tests_source.json"))
    if not files:
        raise FileNotFoundError(f"Missing {dataset} benchmark data")
    return _files_hash(root, files)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _problem_key(dataset: str, problem_id: int) -> str:
    return f"{problem_id:04d}" if dataset == "apps" else f"HumanEval/{problem_id}"


def _smoke_id(root: Path, dataset: str, ids: list[int]) -> int:
    if dataset == "humaneval":
        return min(ids)
    return min(
        ids,
        key=lambda problem_id: (
            len(json.loads((root / "data/apps/raw/test" / f"{problem_id:04d}" / "input_output.json").read_text(encoding="utf-8"))["inputs"]),
            problem_id,
        ),
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resumable native RethinkMCTS cohort runner")
    parser.add_argument("--dataset", choices=("apps", "humaneval", "all"), default="all")
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--evaluator-model", help="Separate model used only for Dual self-evaluation")
    parser.add_argument("--apps-sample-file", type=Path, default=SAMPLES["apps"],
                        help="Locked APPS cohort manifest (benchmark_v2 or 30-item pilot)")
    parser.add_argument("--rollouts", type=int, default=2)
    parser.add_argument("--width", type=int, default=3)
    parser.add_argument("--reward-mode", choices=("dual", "test_only"), default="dual")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-rethink-times", type=int, default=2)
    parser.add_argument("--public-cases-type", default="half",
                        help="APPS public split: half (upstream), half_min2, or an explicit count")
    parser.add_argument("--timeout-seconds", type=float, default=5.0)
    parser.add_argument("--apps-test-workers", type=int, default=1,
                        help="Concurrent APPS tests within one candidate")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top-p", type=float, default=0.95)
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--problem-timeout-seconds", type=float, default=900.0)
    parser.add_argument("--workers", type=int, default=1, help="Independent problems to search concurrently")
    parser.add_argument("--max-consecutive-failures", type=int, default=3)
    parser.add_argument("--data-root", type=Path, default=ROOT / "data")
    parser.add_argument("--output-root", type=Path, default=ROOT / "outputs/rethinkmcts")
    parser.add_argument("--attempt-root", type=Path, default=ROOT / "outputs/rethinkmcts_attempts")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--problem-ids", nargs="+", type=int,
                        help="Run only these IDs from the selected dataset's locked cohort")
    parser.add_argument("--smoke", action="store_true", help="One short APPS case and HumanEval/0")
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--confirm-full-run", action="store_true")
    args = parser.parse_args(argv)
    if _safe_component(args.run_name) != args.run_name:
        parser.error("--run-name must be a safe directory name")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    if args.smoke and args.limit is not None:
        parser.error("--smoke and --limit cannot be combined")
    if args.problem_ids and (args.dataset == "all" or args.limit is not None or args.smoke):
        parser.error("--problem-ids requires one dataset and cannot be combined with --limit or --smoke")
    if args.problem_ids and len(args.problem_ids) != len(set(args.problem_ids)):
        parser.error("--problem-ids must be unique")
    if args.problem_timeout_seconds <= 0 or args.max_consecutive_failures < 1 or args.workers < 1:
        parser.error("problem timeout, workers and max consecutive failures must be positive")
    SearchConfig(
        run_name=args.run_name, model=args.model, evaluator_model=args.evaluator_model, rollouts=args.rollouts,
        width=args.width, reward_mode=args.reward_mode, seed=args.seed, max_rethink_times=args.max_rethink_times,
        public_cases_type=args.public_cases_type,
        timeout_seconds=args.timeout_seconds, temperature=args.temperature,
        apps_test_workers=args.apps_test_workers,
        top_p=args.top_p, max_tokens=args.max_tokens,
    ).validate()
    args.data_root = args.data_root.resolve()
    args.output_root = args.output_root.resolve()
    args.attempt_root = args.attempt_root.resolve()
    return args


def _config(args: argparse.Namespace, root: Path, manifests: dict[str, dict[str, Any]], sample_paths: dict[str, Path]) -> dict[str, Any]:
    search = SearchConfig(
        run_name=args.run_name, model=args.model, evaluator_model=args.evaluator_model, rollouts=args.rollouts,
        width=args.width, reward_mode=args.reward_mode, seed=args.seed, max_rethink_times=args.max_rethink_times,
        public_cases_type=args.public_cases_type,
        timeout_seconds=args.timeout_seconds, temperature=args.temperature,
        apps_test_workers=args.apps_test_workers,
        top_p=args.top_p, max_tokens=args.max_tokens,
    )
    return {
        "schema_version": 1,
        "method": "RethinkMCTS",
        "run_name": args.run_name,
        "model": args.model,
        "search": asdict(search),
        "batch": {
            "workers": args.workers,
            "problem_timeout_seconds": args.problem_timeout_seconds,
            "max_consecutive_failures": args.max_consecutive_failures,
        },
        "cohorts": {
            dataset: {
                "sample_id": manifest["sample_id"],
                "size": len(manifest["problem_ids"]),
                "manifest": sample_paths[dataset].relative_to(root).as_posix(),
                "manifest_sha256": _sha256(sample_paths[dataset]),
                "test_data_sha256": _data_hash(root, dataset, manifest["problem_ids"]),
            }
            for dataset, manifest in manifests.items()
        },
        "execution": {
            "provider": os.getenv("LLM_PROVIDER", "ollama"),
            "model_digest": os.getenv("OLLAMA_MODEL_DIGEST"),
            "evaluator_model_digest": os.getenv("OLLAMA_EVALUATOR_MODEL_DIGEST"),
            "gpu_type": os.getenv("RETHINKMCTS_GPU_TYPE"),
            "image_id": os.getenv("RETHINKMCTS_IMAGE_ID"),
            "modal_inference_sha256": os.getenv("MODAL_INFERENCE_SHA256") if os.getenv("LLM_PROVIDER") == "modal_gpu" else None,
            "python_version": platform.python_version(),
            "source_sha256": _source_hash(root),
        },
    }


def _validated_summary(path: Path, config: dict[str, Any], dataset: str, key: str) -> dict[str, Any] | None:
    summary_path = path / "search_summary.json"
    solution_path = path / "final_solution.py"
    if not summary_path.is_file() or not solution_path.is_file() or not solution_path.read_text(encoding="utf-8").strip():
        return None
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if any((summary.get("run_name") != config["run_name"], summary.get("model") != config["model"],
            summary.get("dataset") != dataset, summary.get("problem_id") != key,
            summary.get("config") != config["search"])):
        raise ValueError(f"Completed search has different identity or parameters: {path}")
    return summary


def _run_one(args: argparse.Namespace, config: dict[str, Any], dataset: str, key: str, number: int) -> dict[str, Any]:
    model_dir = _safe_component(args.model)
    attempt_base = args.attempt_root / args.run_name / model_dir / dataset / _safe_component(key)
    attempt_root = attempt_base / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    attempt_root.mkdir(parents=True, exist_ok=False)
    output = args.output_root / args.run_name / model_dir / dataset / _safe_component(key)
    command = [
        sys.executable, "-m", "rethinkmcts", "--dataset", dataset, "--problem-id", key,
        "--run-name", args.run_name, "--model", args.model,
        "--rollouts", str(args.rollouts), "--width", str(args.width),
        "--reward-mode", args.reward_mode,
        "--seed", str(args.seed), "--max-rethink-times", str(args.max_rethink_times),
        "--public-cases-type", args.public_cases_type,
        "--timeout-seconds", str(args.timeout_seconds),
        "--apps-test-workers", str(args.apps_test_workers),
        "--temperature", str(args.temperature), "--top-p", str(args.top_p),
        "--data-root", str(args.data_root), "--output-root", str(attempt_root),
    ]
    if args.evaluator_model:
        command.extend(("--evaluator-model", args.evaluator_model))
    if args.max_tokens is not None:
        command.extend(("--max-tokens", str(args.max_tokens)))
    started = time.perf_counter()
    status = "failed"
    error = None
    with (attempt_root / "attempt.log").open("w", encoding="utf-8") as log:
        try:
            process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                       start_new_session=(os.name == "posix"))
            try:
                return_code = process.wait(timeout=args.problem_timeout_seconds)
            except subprocess.TimeoutExpired:
                if os.name == "posix":
                    os.killpg(process.pid, signal.SIGKILL)
                else:
                    process.kill()
                process.wait()
                return_code = None
                status = "timeout"
                error = f"Problem exceeded {args.problem_timeout_seconds} seconds"
            if return_code is not None:
                candidate = attempt_root / args.run_name / model_dir / dataset / _safe_component(key)
                if return_code == 0 and _validated_summary(candidate, config, dataset, key) is not None:
                    output.parent.mkdir(parents=True, exist_ok=True)
                    if output.exists():
                        raise FileExistsError(f"Refusing to replace existing MCTS artifact: {output}")
                    candidate.rename(output)
                    status = "completed"
                else:
                    error = f"Search subprocess exited with code {return_code}"
        except (OSError, ValueError) as exc:
            error = f"{type(exc).__name__}: {exc}"
        if error:
            log.write(f"\nBATCH ERROR: {error}\n")
    return {
        "dataset": dataset, "problem_id": key, "attempt": number,
        "status": status, "error": error,
        "duration_seconds": round(time.perf_counter() - started, 3),
        "attempt_dir": str(attempt_root), "artifact_dir": str(output) if status == "completed" else None,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.data_root.parent
    if args.data_root != root / "data":
        raise ValueError("Batch data-root must be a project root/data directory")
    sample_paths = _sample_paths(args)
    manifests = {dataset: load_sample_manifest(sample_paths[dataset], dataset=dataset) for dataset in SAMPLES}
    validate_cohort(manifests)
    config = _config(args, root, manifests, sample_paths)
    model_dir = _safe_component(args.model)
    run_dir = args.output_root / args.run_name / model_dir
    selections: dict[str, list[int]] = {}
    for dataset in (("apps", "humaneval") if args.dataset == "all" else (args.dataset,)):
        ids = manifests[dataset]["problem_ids"]
        if args.problem_ids:
            unknown = set(args.problem_ids) - set(ids)
            if unknown:
                raise ValueError(f"IDs outside the locked {dataset} cohort: {sorted(unknown)}")
            selections[dataset] = [problem_id for problem_id in ids if problem_id in args.problem_ids]
        else:
            selections[dataset] = ([_smoke_id(root, dataset, ids)] if args.smoke else ids[:args.limit] if args.limit else ids)
    pending = []
    completed = 0
    for dataset, ids in selections.items():
        for problem_id in ids:
            key = _problem_key(dataset, problem_id)
            path = run_dir / dataset / _safe_component(key)
            if _validated_summary(path, config, dataset, key) is not None:
                completed += 1
            elif path.exists():
                raise RuntimeError(f"Incomplete artifact at canonical path; preserve and inspect it before retry: {path}")
            else:
                pending.append((dataset, key))
    print(json.dumps({
        "run_name": args.run_name, "model": args.model, "selected": {name: len(ids) for name, ids in selections.items()},
        "completed": completed, "pending": len(pending), "smoke": args.smoke,
        "rollouts": args.rollouts, "width": args.width, "reward_mode": args.reward_mode,
        "evaluator_model": args.evaluator_model,
        "workers": args.workers,
        "public_cases_type": args.public_cases_type,
        "apps_test_workers": args.apps_test_workers,
        "problem_timeout_seconds": args.problem_timeout_seconds,
        "llm_request_estimate_if_all_pass_public": len(pending) * (
            2 if args.reward_mode == "test_only" else 3
        ) * args.rollouts,
        "llm_request_estimate_if_all_fail_public": len(pending) * (
            (3 + 3 * args.max_rethink_times) * args.rollouts + max(args.rollouts - 1, 0)
        ),
    }, ensure_ascii=False, indent=2), flush=True)
    if args.plan:
        return 0
    if len(pending) > 2 and not args.confirm_full_run:
        raise SystemExit("Refusing more than two MCTS searches without --confirm-full-run")
    config_path = run_dir / "run_config.json"
    if config_path.is_file():
        if json.loads(config_path.read_text(encoding="utf-8")) != config:
            raise ValueError(f"Run parameters, cohort, model or code changed; choose a new run name: {config_path}")
    else:
        _write_json(config_path, config)
    progress_path = run_dir / "progress.jsonl"
    failures = 0

    def record(position: int, dataset: str, key: str, result: dict[str, Any]) -> None:
        with progress_path.open("a", encoding="utf-8") as output:
            output.write(json.dumps(result, ensure_ascii=False) + "\n")
        print(f"[{position}/{len(pending)}] {dataset}/{key}: {result['status']}", flush=True)

    if args.workers == 1:
        for position, (dataset, key) in enumerate(pending, 1):
            print(f"[{position}/{len(pending)}] {dataset}/{key}: searching", flush=True)
            result = _run_one(args, config, dataset, key, position)
            record(position, dataset, key, result)
            failures = 0 if result["status"] == "completed" else failures + 1
            if failures >= args.max_consecutive_failures:
                print("Stopping after repeated failures; inspect attempt logs before resuming.", file=sys.stderr)
                return 1
        return 0

    next_position = 0
    in_flight = {}
    stopped = False
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        while next_position < len(pending) or in_flight:
            while not stopped and next_position < len(pending) and len(in_flight) < args.workers:
                dataset, key = pending[next_position]
                next_position += 1
                print(f"[{next_position}/{len(pending)}] {dataset}/{key}: searching", flush=True)
                future = pool.submit(_run_one, args, config, dataset, key, next_position)
                in_flight[future] = (next_position, dataset, key)
            if not in_flight:
                break
            done, _ = wait(in_flight, return_when=FIRST_COMPLETED)
            for future in done:
                position, dataset, key = in_flight.pop(future)
                try:
                    result = future.result()
                except Exception as exc:
                    result = {
                        "dataset": dataset, "problem_id": key, "attempt": position,
                        "status": "failed", "error": f"{type(exc).__name__}: {exc}",
                        "artifact_dir": None,
                        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
                    }
                record(position, dataset, key, result)
                failures = 0 if result["status"] == "completed" else failures + 1
                if failures >= args.max_consecutive_failures:
                    stopped = True
    if stopped:
        print("Stopping after repeated failures; inspect attempt logs before resuming.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
