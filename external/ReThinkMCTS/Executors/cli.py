from __future__ import annotations

import argparse
from pathlib import Path

from . import AppsExecutor, HumanevalExecutor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate generated Python code.")
    parser.add_argument("--dataset", required=True, choices=("apps", "humaneval"))
    parser.add_argument("--problem-id", required=True)
    parser.add_argument("--code-file", required=True, type=Path)
    parser.add_argument("--split", default="test", choices=("train", "test"))
    parser.add_argument("--timeout", type=float, default=None)
    parser.add_argument("--test-workers", type=int, default=1)
    parser.add_argument("--max-tests", type=int, default=None)
    parser.add_argument("--report-file", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    code = args.code_file.read_text(encoding="utf-8")
    if args.dataset == "apps":
        executor = AppsExecutor(
            timeout_per_test=args.timeout or 2.0,
            test_workers=args.test_workers,
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
        executor = HumanevalExecutor(timeout=args.timeout or 5.0)
        report = executor.evaluate(code, args.problem_id)

    report_json = report.to_json()
    print(report_json)
    if args.report_file:
        args.report_file.parent.mkdir(parents=True, exist_ok=True)
        args.report_file.write_text(report_json + "\n", encoding="utf-8")
    return 0 if report.status == "passed" else 1
