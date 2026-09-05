import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from sandbox.executor import CodeExecutor
from data.schemas import TestCase, TestStatus


class TestCodeExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = CodeExecutor(timeout=1.0)

    def test_accepted(self):
        code = "a, b = map(int, input().split())\nprint(a + b)"
        test = TestCase(input="3 5\n", output="8\n")
        res = self.executor.run_single_test(code, test)
        self.assertEqual(res.status, TestStatus.ACCEPTED)

    def test_wrong_answer(self):
        code = "a, b = map(int, input().split())\nprint(a - b)"
        test = TestCase(input="3 5\n", output="8\n")
        res = self.executor.run_single_test(code, test)
        self.assertEqual(res.status, TestStatus.WRONG_ANSWER)
        self.assertIn("Output mismatch", res.error_message)

    def test_time_limit_exceeded(self):
        code = "import time\nwhile True:\n    time.sleep(0.1)"
        test = TestCase(input="1\n", output="1\n")
        res = self.executor.run_single_test(code, test)
        self.assertEqual(res.status, TestStatus.TIME_LIMIT_EXCEEDED)

    def test_runtime_error(self):
        code = "print(1 / 0)"
        test = TestCase(input="1\n", output="1\n")
        res = self.executor.run_single_test(code, test)
        self.assertEqual(res.status, TestStatus.RUNTIME_ERROR)
        self.assertIn("ZeroDivisionError", res.error_message)


if __name__ == "__main__":
    unittest.main()
