"""Keep Modal MCTS problem workers busy while recording individual failures."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

from baselines.sample_selection import load_sample_manifest
from rethinkmcts import batch
from tools.modal_mcts.inference import APP_NAME, EVALUATOR_MODEL, MODEL


def run_queue(pending: list[tuple[str, str]], workers: int, run_one, record) -> None:
    """Submit a new problem whenever any worker becomes free."""
    iterator = iter(enumerate(pending, 1))
    in_flight = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        while True:
            while len(in_flight) < workers:
                item = next(iterator, None)
                if item is None:
                    break
                position, (dataset, key) = item
                print(f"[{position}/{len(pending)}] {dataset}/{key}: searching", flush=True)
                in_flight[pool.submit(run_one, position, dataset, key)] = (position, dataset, key)
            if not in_flight:
                break
            done, _ = wait(in_flight, return_when=FIRST_COMPLETED)
            for future in done:
                position, dataset, key = in_flight.pop(future)
                try:
                    result = future.result()
                except Exception as exc:
                    result = {"dataset": dataset, "problem_id": key, "status": "failed",
                              "error": f"{type(exc).__name__}: {exc}"}
                record(position, dataset, key, result)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=("apps", "humaneval"), required=True)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--reward-mode", choices=("dual", "test_only"), required=True)
    parser.add_argument("--expected-model-digest", required=True)
    parser.add_argument("--evaluator-model")
    parser.add_argument("--expected-evaluator-model-digest")
    parser.add_argument("--apps-sample-file", type=Path, default=batch.SAMPLES["apps"])
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args(argv)
    if not 1 <= args.workers <= 4:
        parser.error("--workers must be between 1 and 4")
    if args.evaluator_model:
        if args.evaluator_model != EVALUATOR_MODEL or args.reward_mode != "dual":
            parser.error("External evaluator requires Dual and the allow-listed 14B model")
        if not args.expected_evaluator_model_digest:
            parser.error("--expected-evaluator-model-digest is required with --evaluator-model")

    os.environ["LLM_PROVIDER"] = "modal_gpu"
    os.environ["LLM_MODEL"] = MODEL
    os.environ["MODAL_INFERENCE_SHA256"] = hashlib.sha256(
        (Path(__file__).parent / "inference.py").read_bytes()
    ).hexdigest()

    import modal

    info = modal.Cls.from_name(APP_NAME, "OllamaInference")().model_info.remote(bool(args.evaluator_model))
    if (info.get("model") != MODEL or info.get("digest") != args.expected_model_digest
            or "L40S" not in info.get("gpu", "")):
        raise RuntimeError(f"Modal model identity differs from the pinned run: {info}")
    os.environ["OLLAMA_MODEL_DIGEST"] = info["digest"]
    if args.evaluator_model:
        evaluator_digest = info.get("models", {}).get(args.evaluator_model, {}).get("digest")
        if evaluator_digest != args.expected_evaluator_model_digest:
            raise RuntimeError("Modal evaluator digest differs from the pinned run")
        os.environ["OLLAMA_EVALUATOR_MODEL_DIGEST"] = evaluator_digest
    os.environ["RETHINKMCTS_GPU_TYPE"] = info["gpu"]
    os.environ["RETHINKMCTS_IMAGE_ID"] = f"modal:{APP_NAME}:{info['ollama_version']}"
    print(json.dumps({"modal_preflight": info}), flush=True)

    batch_args = batch.parse_args([
        "--dataset", args.dataset, "--run-name", args.run_name, "--model", MODEL,
        "--reward-mode", args.reward_mode, "--workers", str(args.workers),
        "--apps-test-workers", "1", "--apps-sample-file", str(args.apps_sample_file), "--confirm-full-run",
    ])
    if args.evaluator_model:
        batch_args.evaluator_model = args.evaluator_model
    root = batch_args.data_root.parent
    sample_paths = batch._sample_paths(batch_args)
    manifests = {dataset: load_sample_manifest(sample_paths[dataset], dataset=dataset)
                 for dataset in batch.SAMPLES}
    batch.validate_cohort(manifests)
    config = batch._config(batch_args, root, manifests, sample_paths)
    run_dir = batch_args.output_root / args.run_name / batch._safe_component(MODEL)
    config_path = run_dir / "run_config.json"
    if not config_path.is_file() or json.loads(config_path.read_text(encoding="utf-8")) != config:
        raise ValueError(f"Existing run parameters or source differ: {config_path}")

    pending = []
    for problem_id in manifests[args.dataset]["problem_ids"]:
        key = batch._problem_key(args.dataset, problem_id)
        path = run_dir / args.dataset / batch._safe_component(key)
        if batch._validated_summary(path, config, args.dataset, key) is not None:
            continue
        if path.exists():
            raise RuntimeError(f"Incomplete artifact at canonical path: {path}")
        pending.append((args.dataset, key))
    print(json.dumps({"pending": len(pending), "workers": args.workers}), flush=True)

    progress_path = run_dir / "progress.jsonl"

    def record(position: int, dataset: str, key: str, result: dict) -> None:
        with progress_path.open("a", encoding="utf-8") as output:
            output.write(json.dumps(result, ensure_ascii=False) + "\n")
        print(f"[{position}/{len(pending)}] {dataset}/{key}: {result['status']}", flush=True)

    run_queue(pending, args.workers,
              lambda position, dataset, key: batch._run_one(batch_args, config, dataset, key, position),
              record)
    remaining = [key for dataset, key in pending if batch._validated_summary(
        run_dir / dataset / batch._safe_component(key), config, dataset, key) is None]
    print(json.dumps({"attempted": len(pending), "remaining": len(remaining),
                      "remaining_ids": remaining}), flush=True)
    return 1 if remaining else 0


if __name__ == "__main__":
    raise SystemExit(main())
