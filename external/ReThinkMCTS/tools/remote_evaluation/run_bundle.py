from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from baselines.direct_generation.pipeline import safe_path_component


ROOT = Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate a staged benchmark-v2 bundle without contacting an LLM")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--apps-timeout", type=float, default=2.0)
    parser.add_argument("--humaneval-timeout", type=float, default=5.0)
    parser.add_argument("--plan", action="store_true")
    args = parser.parse_args(argv)
    if args.workers < 1 or args.apps_timeout <= 0 or args.humaneval_timeout <= 0:
        parser.error("workers and timeouts must be positive")

    info = json.loads((ROOT / "bundle.json").read_text(encoding="utf-8"))
    run_name = info["run_name"]
    model = info["model"]
    record = ROOT / "outputs/benchmarks" / safe_path_component(run_name) / safe_path_component(model) / "run.json"
    if record.is_file() and not args.plan:
        from .collect_results import collect_results

        print(f"Benchmark record already finalized: {record}")
        print(f"Results archive: {collect_results(ROOT, run_name=run_name, model=model)}")
        return 0
    for dataset, timeout in (("apps", args.apps_timeout), ("humaneval", args.humaneval_timeout)):
        manifest = ROOT / (
            "data/samples/benchmark_v2/apps_test_300.json"
            if dataset == "apps" else "data/samples/benchmark_v2/humaneval_test_164.json"
        )
        command = [
            sys.executable, "-m", "evaluation",
            "--dataset", dataset,
            "--run-name", run_name,
            "--model", model,
            "--sample-file", str(manifest),
            "--workers", str(args.workers),
            "--test-workers", "1",
            "--timeout", str(timeout),
            "--confirm-full-run",
        ]
        if args.plan:
            command.append("--plan")
        subprocess.run(command, cwd=ROOT, check=True)
    if not args.plan:
        subprocess.run(
            [sys.executable, "-m", "evaluation.benchmark_judge", "--run-name", run_name, "--model", model],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(
            [sys.executable, "-m", "evaluation.benchmark_record", "--bundle-file", str(ROOT / "bundle.json")],
            cwd=ROOT,
            check=True,
        )
        from .collect_results import collect_results

        print(f"Results archive: {collect_results(ROOT, run_name=run_name, model=model)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
