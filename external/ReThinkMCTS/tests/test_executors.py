from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from Executors import AppsExecutor, HumanevalExecutor


class AppsExecutorTests(unittest.TestCase):
    def _dataset(self, payload: dict) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        problem_dir = Path(temporary.name) / "test" / "0000"
        problem_dir.mkdir(parents=True)
        (problem_dir / "input_output.json").write_text(
            json.dumps(payload), encoding="utf-8"
        )
        return temporary, Path(temporary.name)

    def test_stdin_stdout_reports_partial_pass(self) -> None:
        temporary, root = self._dataset(
            {"inputs": ["2 3\n", "4 5\n"], "outputs": ["5\n", "10\n"]}
        )
        self.addCleanup(temporary.cleanup)
        code = "a, b = map(int, input().split())\nprint(a + b)\n"

        report = AppsExecutor(root).evaluate(code, 0)

        self.assertEqual(report.passed_tests, 1)
        self.assertEqual(report.total_tests, 2)
        self.assertEqual(report.pass_rate, 0.5)
        self.assertEqual(report.tests[1].status, "wrong_answer")

    def test_call_based_supports_solution_method(self) -> None:
        temporary, root = self._dataset(
            {
                "fn_name": "add",
                "inputs": [[2, 3], [4, 5]],
                "outputs": [5, 9],
            }
        )
        self.addCleanup(temporary.cleanup)
        code = "class Solution:\n    def add(self, a, b):\n        return a + b\n"

        report = AppsExecutor(root).evaluate(code, "0000")

        self.assertEqual(report.status, "passed")
        self.assertEqual(report.passed_tests, 2)
        self.assertEqual(report.mode, "call_based")

    def test_timeout_is_reported(self) -> None:
        temporary, root = self._dataset({"inputs": [""], "outputs": [""]})
        self.addCleanup(temporary.cleanup)

        report = AppsExecutor(root, timeout_per_test=0.2).evaluate(
            "while True:\n    pass\n", 0
        )

        self.assertEqual(report.tests[0].status, "timeout")
        self.assertEqual(report.passed_tests, 0)


class HumanEvalExecutorTests(unittest.TestCase):
    def test_official_harness_passes_known_implementation(self) -> None:
        code = '''def has_close_elements(numbers, threshold):
    for index, left in enumerate(numbers):
        for right in numbers[index + 1:]:
            if abs(left - right) < threshold:
                return True
    return False
'''

        report = HumanevalExecutor().evaluate(code, "HumanEval/0")

        self.assertEqual(report.status, "passed")
        self.assertEqual(report.passed_tests, 1)
        self.assertEqual(report.total_tests, 1)
        self.assertEqual(report.mode, "official_harness")

    def test_official_harness_rejects_wrong_implementation(self) -> None:
        report = HumanevalExecutor().evaluate(
            "def has_close_elements(numbers, threshold):\n    return False\n", 0
        )

        self.assertEqual(report.status, "failed")
        self.assertEqual(report.tests[0].status, "wrong_answer")


if __name__ == "__main__":
    unittest.main()
