from __future__ import annotations

import json
import math
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from .common import (
    ExecutionReport,
    TestCaseResult,
    build_report,
    clip_text,
    run_python_file,
    run_python_source,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APPS_ROOT = PROJECT_ROOT / "data" / "apps" / "raw"

CALL_HARNESS = r'''import json
import runpy


def jsonable(value):
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, set):
        return sorted((jsonable(item) for item in value), key=repr)
    return repr(value)


payload = json.loads(open("case.json", encoding="utf-8").read())
namespace = runpy.run_path("candidate.py")
function_name = payload["function_name"]
target = namespace.get(function_name)
if target is None and "Solution" in namespace:
    target = getattr(namespace["Solution"](), function_name)
if not callable(target):
    raise AttributeError(f"Callable {function_name!r} was not found")
arguments = payload["input"]
if not isinstance(arguments, list):
    arguments = [arguments]
result = target(*arguments)
open("result.json", "w", encoding="utf-8").write(
    json.dumps(jsonable(result), ensure_ascii=False, allow_nan=True)
)
'''


def _as_text(value: Any) -> str:
    if isinstance(value, list):
        return "\n".join(str(item) for item in value)
    return str(value)


def _stdout_matches(actual: str, expected: Any) -> bool:
    expected_text = _as_text(expected)
    actual_lines = [line.strip() for line in actual.strip().splitlines()]
    expected_lines = [line.strip() for line in expected_text.strip().splitlines()]
    if actual_lines == expected_lines:
        return True
    return actual.split() == expected_text.split()


def _structured_matches(actual: Any, expected: Any) -> bool:
    if isinstance(actual, bool) or isinstance(expected, bool):
        return actual is expected
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        return math.isclose(float(actual), float(expected), rel_tol=1e-7, abs_tol=1e-7)
    if isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(
            _structured_matches(left, right)
            for left, right in zip(actual, expected)
        )
    if isinstance(actual, dict) and isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            _structured_matches(actual[key], expected[key]) for key in actual
        )
    return actual == expected


def _call_result_matches(actual: Any, expected: Any) -> bool:
    if _structured_matches(actual, expected):
        return True
    return (
        isinstance(expected, list)
        and bool(expected)
        and _structured_matches(actual, expected[0])
    )


class AppsExecutor:
    def __init__(
        self,
        data_root: str | Path = DEFAULT_APPS_ROOT,
        *,
        timeout_per_test: float = 2.0,
        test_workers: int = 1,
        python_executable: str | Path = sys.executable,
    ) -> None:
        self.data_root = Path(data_root)
        self.timeout_per_test = timeout_per_test
        if test_workers <= 0:
            raise ValueError("test_workers must be greater than zero")
        self.test_workers = test_workers
        self.python_executable = python_executable

    def evaluate(
        self,
        code: str,
        problem_id: str | int,
        *,
        split: str = "test",
        max_tests: int | None = None,
        test_indices: list[int] | None = None,
    ) -> ExecutionReport:
        if split not in {"train", "test"}:
            raise ValueError("APPS split must be 'train' or 'test'")
        numeric_id = int(problem_id)
        tests_path = self.data_root / split / f"{numeric_id:04d}" / "input_output.json"
        if not tests_path.is_file():
            raise FileNotFoundError(f"APPS tests not found: {tests_path}")

        payload = json.loads(tests_path.read_text(encoding="utf-8"))
        inputs = payload.get("inputs", [])
        outputs = payload.get("outputs", [])
        if not isinstance(inputs, list) or not isinstance(outputs, list):
            raise ValueError(f"Invalid APPS test schema: {tests_path}")
        if len(inputs) != len(outputs):
            raise ValueError("APPS inputs and outputs must have the same length")
        if max_tests is not None and test_indices is not None:
            raise ValueError("max_tests and test_indices are mutually exclusive")
        if test_indices is not None:
            if any(index < 0 or index >= len(inputs) for index in test_indices):
                raise ValueError("test_indices contains an out-of-range test")
            selected = [(inputs[index], outputs[index]) for index in test_indices]
            selected_indices = list(test_indices)
        elif max_tests is not None:
            if max_tests <= 0:
                raise ValueError("max_tests must be greater than zero")
            selected = list(zip(inputs, outputs))[:max_tests]
            selected_indices = list(range(len(selected)))
        else:
            selected = list(zip(inputs, outputs))
            selected_indices = list(range(len(selected)))

        function_name = payload.get("fn_name")
        mode = "call_based" if function_name else "stdin_stdout"
        def run_case(item: tuple[int, tuple[Any, Any]]) -> TestCaseResult:
            index, (test_input, expected) = item
            if function_name:
                return self._run_call_case(
                    code, index, function_name, test_input, expected
                )
            return self._run_stdin_case(code, index, test_input, expected)

        indexed_cases = list(zip(selected_indices, selected))
        if self.test_workers == 1 or len(indexed_cases) <= 1:
            results = [run_case(item) for item in indexed_cases]
        else:
            # Each test owns its temporary directory/process, so APPS cases can
            # run concurrently without sharing candidate state or output files.
            with ThreadPoolExecutor(max_workers=self.test_workers) as pool:
                results = list(pool.map(run_case, indexed_cases))

        return build_report(
            dataset="apps",
            problem_id=f"{numeric_id:04d}",
            mode=mode,
            available_tests=len(inputs),
            tests=results,
        )

    def _run_stdin_case(
        self, code: str, index: int, test_input: Any, expected: Any
    ) -> TestCaseResult:
        process = run_python_source(
            code,
            stdin=_as_text(test_input),
            timeout_seconds=self.timeout_per_test,
            python_executable=self.python_executable,
        )
        if process.status == "timeout":
            return TestCaseResult(
                index=index,
                status="timeout",
                passed=False,
                duration_seconds=process.duration_seconds,
                expected=expected,
                actual=clip_text(process.stdout),
                error="Execution exceeded the per-test timeout",
            )
        if process.returncode != 0:
            return TestCaseResult(
                index=index,
                status="runtime_error",
                passed=False,
                duration_seconds=process.duration_seconds,
                expected=expected,
                actual=clip_text(process.stdout),
                error=clip_text(process.stderr),
            )
        passed = _stdout_matches(process.stdout, expected)
        return TestCaseResult(
            index=index,
            status="passed" if passed else "wrong_answer",
            passed=passed,
            duration_seconds=process.duration_seconds,
            expected=expected,
            actual=clip_text(process.stdout),
        )

    def _run_call_case(
        self,
        code: str,
        index: int,
        function_name: str,
        test_input: Any,
        expected: Any,
    ) -> TestCaseResult:
        with tempfile.TemporaryDirectory(prefix="rethinkmcts-apps-call-") as temp_dir:
            root = Path(temp_dir)
            (root / "candidate.py").write_text(code, encoding="utf-8")
            (root / "case.json").write_text(
                json.dumps(
                    {"function_name": function_name, "input": test_input},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            harness_path = root / "harness.py"
            harness_path.write_text(CALL_HARNESS, encoding="utf-8")
            process = run_python_file(
                harness_path,
                timeout_seconds=self.timeout_per_test,
                python_executable=self.python_executable,
            )
            result_path = root / "result.json"
            if process.status == "timeout":
                status = "timeout"
                error = "Execution exceeded the per-test timeout"
                actual = None
            elif process.returncode != 0 or not result_path.is_file():
                status = "runtime_error"
                error = clip_text(process.stderr or "Candidate produced no result")
                actual = None
            else:
                actual = json.loads(result_path.read_text(encoding="utf-8"))
                passed = _call_result_matches(actual, expected)
                status = "passed" if passed else "wrong_answer"
                error = None
            return TestCaseResult(
                index=index,
                status=status,
                passed=status == "passed",
                duration_seconds=process.duration_seconds,
                expected=expected,
                actual=actual,
                error=error,
            )
