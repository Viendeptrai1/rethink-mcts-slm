from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import SearchConfig
from .runner import DEFAULT_DATA_ROOT, DEFAULT_OUTPUT_ROOT, load_context, run_search


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run native RethinkMCTS on one problem.")
    parser.add_argument("--dataset", required=True, choices=["apps", "humaneval"])
    parser.add_argument("--problem-id", required=True)
    parser.add_argument("--run-name", default="rethinkmcts_v1")
    parser.add_argument("--model", default=None)
    parser.add_argument("--evaluator-model", default=None,
                        help="Optional separate model used only for Dual self-evaluation")
    parser.add_argument("--rollouts", type=int, default=16)
    parser.add_argument("--width", type=int, default=3)
    parser.add_argument("--reward-mode", choices=("dual", "test_only"), default="dual")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--c-base", type=float, default=10.0)
    parser.add_argument("--exploration-weight", type=float, default=4.0)
    parser.add_argument("--public-cases-type", default="half",
                        help="APPS public split: half (upstream), half_min2, or an explicit count")
    parser.add_argument("--max-rethink-times", type=int, default=2)
    parser.add_argument("--timeout-seconds", type=float, default=5.0)
    parser.add_argument("--apps-test-workers", type=int, default=1,
                        help="Concurrent APPS tests within one candidate")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top-p", type=float, default=0.95)
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--plan", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = SearchConfig(
        run_name=args.run_name,
        model=args.model,
        evaluator_model=args.evaluator_model,
        rollouts=args.rollouts,
        width=args.width,
        reward_mode=args.reward_mode,
        seed=args.seed,
        c_base=args.c_base,
        exploration_weight=args.exploration_weight,
        public_cases_type=args.public_cases_type,
        max_rethink_times=args.max_rethink_times,
        timeout_seconds=args.timeout_seconds,
        apps_test_workers=args.apps_test_workers,
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
    )
    config.validate()
    context = load_context(
        args.dataset,
        args.problem_id,
        data_root=args.data_root,
        public_cases_type=args.public_cases_type,
    )
    print(json.dumps({"config": config.__dict__, "problem": context.to_dict()}, ensure_ascii=False, indent=2))
    if args.plan:
        return 0
    result = run_search(
        context=context,
        config=config,
        data_root=args.data_root,
        output_root=args.output_root,
    )
    print(json.dumps({
        "best_candidate_id": result.best_candidate.candidate_id if result.best_candidate else None,
        "best_reward": result.best_candidate.reward if result.best_candidate else None,
        "output_root": str(args.output_root),
    }, ensure_ascii=False))
    return 0
