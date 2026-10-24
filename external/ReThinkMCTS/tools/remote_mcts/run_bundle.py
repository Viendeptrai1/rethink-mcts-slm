from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from urllib.request import urlopen

from baselines.sample_selection import load_sample_manifest
from rethinkmcts import batch
from rethinkmcts.benchmark import finalize_benchmark
from tools.gpu.run_generation import _models, _pull_model


ROOT = Path(__file__).resolve().parents[2]
OLLAMA_URL = "http://127.0.0.1:11434"


def _model_digest(model: str) -> str:
    with urlopen(f"{OLLAMA_URL}/api/tags", timeout=10) as response:
        payload = json.load(response)
    for entry in payload.get("models", []):
        if entry.get("name") == model or entry.get("model") == model:
            digest = str(entry.get("digest") or "")
            if digest:
                return digest
    raise RuntimeError(f"Ollama did not report a digest for {model}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan, smoke, or resume the exact remote RethinkMCTS cohort")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plan", action="store_true")
    mode.add_argument("--smoke", action="store_true")
    mode.add_argument("--confirm-full-run", action="store_true")
    parser.add_argument("--rollouts", type=int, default=2)
    parser.add_argument("--width", type=int, default=3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-rethink-times", type=int, default=2)
    parser.add_argument("--timeout-seconds", type=float, default=5.0)
    parser.add_argument("--problem-timeout-seconds", type=float, default=900.0)
    parser.add_argument("--max-tokens", type=int)
    args = parser.parse_args(argv)
    info = json.loads((ROOT / "bundle.json").read_text(encoding="utf-8"))
    if info.get("method") != "RethinkMCTS" or info["cohorts"]["apps"]["count"] != 300 or info["cohorts"]["humaneval"]["count"] != 164:
        raise ValueError("Not an exact RethinkMCTS 300+164 bundle")
    if info["source_sha256"] != batch._source_hash(ROOT):
        raise ValueError("Bundle source changed after packaging")
    for dataset, relative in batch.SAMPLES.items():
        if info["cohorts"][dataset]["manifest_sha256"] != batch._sha256(ROOT / relative):
            raise ValueError(f"{dataset} manifest changed after packaging")
        manifest = load_sample_manifest(ROOT / relative, dataset=dataset)
        if info["cohorts"][dataset]["test_data_sha256"] != batch._data_hash(ROOT, dataset, manifest["problem_ids"]):
            raise ValueError(f"{dataset} test data changed after packaging")
    model = info["model"]
    common = [
        "--dataset", "all", "--run-name", info["run_name"], "--model", model,
        "--rollouts", str(args.rollouts), "--width", str(args.width),
        "--seed", str(args.seed), "--max-rethink-times", str(args.max_rethink_times),
        "--timeout-seconds", str(args.timeout_seconds),
        "--problem-timeout-seconds", str(args.problem_timeout_seconds),
    ]
    if args.max_tokens is not None:
        common.extend(("--max-tokens", str(args.max_tokens)))
    if args.plan:
        return batch.main([*common, "--plan"])
    if model not in _models(OLLAMA_URL):
        _pull_model(OLLAMA_URL, model)
    os.environ["LLM_MODEL"] = model
    os.environ["OLLAMA_MODEL_DIGEST"] = _model_digest(model)
    status = batch.main([*common, "--smoke" if args.smoke else "--confirm-full-run"])
    if status or args.smoke:
        return status
    print(f"Benchmark report: {finalize_benchmark(root=ROOT, run_name=info['run_name'], model=model)}")
    from .collect_results import collect_results

    print(f"Results archive: {collect_results(root=ROOT, run_name=info['run_name'], model=model)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
