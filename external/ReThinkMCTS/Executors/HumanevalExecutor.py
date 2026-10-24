from __future__ import annotations

import sys
from pathlib import Path

from .common import ExecutionReport, TestCaseResult, build_report, clip_text, run_python_source


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HUMANEVAL_PATH = PROJECT_ROOT / "data" / "humaneval" / "arrow"


class HumanevalExecutor:
    def __init__(
        self,
        data_path: str | Path = DEFAULT_HUMANEVAL_PATH,
        *,
        timeout: float = 5.0,
        python_executable: str | Path = sys.executable,
    ) -> None:
        self.data_path = Path(data_path)
        self.timeout = timeout
        self.python_executable = python_executable

    def evaluate(self, code: str, problem_id: str | int) -> ExecutionReport:
        try:
            numeric_id = int(str(problem_id).removeprefix("HumanEval/"))
        except ValueError as exc:
            raise ValueError(
                "HumanEval problem_id must be an integer or HumanEval/<id>"
            ) from exc
        if not self.data_path.is_dir():
            raise FileNotFoundError(f"HumanEval dataset not found: {self.data_path}")

        from datasets import load_from_disk

        dataset = load_from_disk(str(self.data_path))["test"]
        if numeric_id < 0 or numeric_id >= len(dataset):
            raise ValueError(f"HumanEval problem_id must be between 0 and {len(dataset) - 1}")
        row = dataset[numeric_id]
        source = "\n\n".join(
            (code.rstrip(), row["test"].rstrip(), f"check({row['entry_point']})")
        ) + "\n"
        process = run_python_source(
            source,
            timeout_seconds=self.timeout,
            python_executable=self.python_executable,
        )
        if process.status == "timeout":
            status = "timeout"
            error = "Execution exceeded the HumanEval harness timeout"
        elif process.returncode != 0:
            status = (
                "wrong_answer"
                if "AssertionError" in process.stderr
                else "runtime_error"
            )
            error = clip_text(process.stderr)
        else:
            status = "passed"
            error = None
        test = TestCaseResult(
            index=0,
            status=status,
            passed=status == "passed",
            duration_seconds=process.duration_seconds,
            actual=clip_text(process.stdout) or None,
            error=error,
        )
        return build_report(
            dataset="humaneval",
            problem_id=row["task_id"],
            mode="official_harness",
            available_tests=1,
            tests=[test],
        )
