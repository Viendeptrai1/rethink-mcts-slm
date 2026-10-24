"""Run the local MCTS judge with authenticated Modal GPU inference."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from rethinkmcts import batch
from tools.modal_mcts.inference import APP_NAME, EVALUATOR_MODEL, MODEL


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local judge + Modal GPU LLM for fixed MCTS cohort")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plan", action="store_true")
    mode.add_argument("--preflight", action="store_true", help="Pull/check requested models and print digests without searching")
    mode.add_argument("--smoke", action="store_true", help="One APPS and one HumanEval problem")
    mode.add_argument("--confirm-full-run", action="store_true")
    parser.add_argument("--dataset", choices=("apps", "humaneval", "all"), default="all")
    parser.add_argument("--limit", type=int, help="First N IDs in each selected cohort, for staged runs")
    parser.add_argument("--problem-ids", nargs="+", type=int,
                        help="Only these IDs from the selected dataset's locked cohort")
    parser.add_argument("--run-name", default="rethinkmcts_qwen25_modal_l40s_parallel_v1")
    parser.add_argument("--rollouts", type=int, default=2)
    parser.add_argument("--width", type=int, default=3)
    parser.add_argument("--reward-mode", choices=("dual", "test_only"), default="dual")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-rethink-times", type=int, default=2)
    parser.add_argument("--public-cases-type", default="half",
                        help="APPS public split: half, half_min2, or an explicit count")
    parser.add_argument("--timeout-seconds", type=float, default=5.0)
    parser.add_argument("--apps-test-workers", type=int, default=1,
                        help="Concurrent APPS tests within one candidate")
    parser.add_argument("--problem-timeout-seconds", type=float, default=900.0)
    parser.add_argument("--workers", type=int, default=1, help="Concurrent problems (maximum 4 Modal replicas)")
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--expected-model-digest", help="Abort if Modal serves a different model revision")
    parser.add_argument("--evaluator-model", help="Optional model used only to produce Dual v_llm")
    parser.add_argument("--expected-evaluator-model-digest", help="Required with evaluator-model for a real run")
    parser.add_argument("--apps-sample-file", type=Path,
                        default=Path("data/samples/benchmark_v2/apps_test_300.json"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not 1 <= args.workers <= 4:
        raise ValueError("--workers must be between 1 and 4 for this Modal deployment")
    if args.evaluator_model:
        if args.evaluator_model != EVALUATOR_MODEL:
            raise ValueError(f"This deployment only allow-lists evaluator model {EVALUATOR_MODEL}")
        if args.reward_mode != "dual":
            raise ValueError("--evaluator-model requires --reward-mode dual")
        if not args.plan and not args.preflight and (not args.expected_model_digest or not args.expected_evaluator_model_digest):
            raise ValueError("Real runs with an external evaluator require both expected model digests")
    if args.run_name == "rethinkmcts_qwen25_modal_v1" and not args.plan:
        raise ValueError("The L4 run is immutable; use a new run name for the L40S deployment")
    os.environ["LLM_PROVIDER"] = "modal_gpu"
    os.environ["LLM_MODEL"] = MODEL
    os.environ.pop("OLLAMA_EVALUATOR_MODEL_DIGEST", None)
    os.environ["MODAL_INFERENCE_SHA256"] = hashlib.sha256(
        (Path(__file__).parent / "inference.py").read_bytes()
    ).hexdigest()
    common = [
        "--dataset", args.dataset, "--run-name", args.run_name, "--model", MODEL,
        "--apps-sample-file", str(args.apps_sample_file),
        "--rollouts", str(args.rollouts), "--width", str(args.width),
        "--reward-mode", args.reward_mode,
        "--seed", str(args.seed), "--max-rethink-times", str(args.max_rethink_times),
        "--public-cases-type", args.public_cases_type,
        "--timeout-seconds", str(args.timeout_seconds),
        "--apps-test-workers", str(args.apps_test_workers),
        "--problem-timeout-seconds", str(args.problem_timeout_seconds),
        "--workers", str(args.workers),
    ]
    if args.evaluator_model:
        common.extend(("--evaluator-model", args.evaluator_model))
    if args.max_tokens is not None:
        common.extend(("--max-tokens", str(args.max_tokens)))
    if args.limit is not None:
        if args.limit < 1 or args.smoke:
            raise ValueError("--limit must be positive and cannot be combined with --smoke")
        common.extend(("--limit", str(args.limit)))
    if args.problem_ids:
        common.extend(("--problem-ids", *(str(problem_id) for problem_id in args.problem_ids)))
    if args.plan:
        return batch.main([*common, "--plan"])

    import modal

    instance = modal.Cls.from_name(APP_NAME, "OllamaInference")()
    info = instance.model_info.remote(bool(args.evaluator_model))
    if info.get("model") != MODEL or not info.get("digest") or not info.get("gpu"):
        raise RuntimeError("Modal GPU model preflight returned incomplete identity")
    if "L40S" not in info["gpu"]:
        raise RuntimeError(f"Expected L40S, Modal reported {info['gpu']}; deploy the new inference.py")
    if args.expected_model_digest and info["digest"] != args.expected_model_digest:
        raise RuntimeError("Modal model digest differs from --expected-model-digest")
    evaluator_digest = None
    if args.evaluator_model:
        evaluator_record = info.get("models", {}).get(args.evaluator_model, {})
        evaluator_digest = evaluator_record.get("digest")
        if not evaluator_digest:
            raise RuntimeError("Modal preflight did not return the evaluator model digest")
        if (args.expected_evaluator_model_digest
                and evaluator_digest != args.expected_evaluator_model_digest):
            raise RuntimeError("Modal evaluator digest differs from --expected-evaluator-model-digest")
    os.environ["OLLAMA_MODEL_DIGEST"] = info["digest"]
    if evaluator_digest:
        os.environ["OLLAMA_EVALUATOR_MODEL_DIGEST"] = evaluator_digest
    os.environ["RETHINKMCTS_GPU_TYPE"] = info["gpu"]
    os.environ["RETHINKMCTS_IMAGE_ID"] = f"modal:{APP_NAME}:{info['ollama_version']}"
    print(json.dumps({"modal_preflight": info}, ensure_ascii=False), flush=True)
    if args.preflight:
        return 0
    return batch.main([*common, "--smoke" if args.smoke else "--confirm-full-run"])


if __name__ == "__main__":
    raise SystemExit(main())
