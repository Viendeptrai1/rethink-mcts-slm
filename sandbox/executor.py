import sys
import time
import subprocess
import tempfile
import os
from typing import List, Tuple
from data.schemas import TestCase, SingleTestResult, ExecutionResult, TestStatus


class CodeExecutor:
    """
    Trình thực thi mã nguồn Python cô lập và an toàn cho các bài toán Competitive Programming.
    Hỗ trợ luồng I/O tiêu chuẩn (stdin -> stdout) và kiểm soát timeout.
    """
    def __init__(self, timeout: float = 2.0, python_executable: str = sys.executable):
        self.timeout = timeout
        self.python_executable = python_executable

    def _normalize_output(self, text: str) -> str:
        """Chuẩn hóa output để so sánh: loại bỏ khoảng trắng thừa ở cuối mỗi dòng và đầu/cuối chuỗi."""
        lines = [line.rstrip() for line in text.strip().splitlines()]
        return "\n".join(lines)

    def run_single_test(self, code: str, test_case: TestCase) -> SingleTestResult:
        """Chạy một test case cụ thể với mã nguồn được cung cấp."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp_file:
            tmp_file.write(code)
            tmp_path = tmp_file.name

        start_time = time.time()
        try:
            process = subprocess.run(
                [self.python_executable, tmp_path],
                input=test_case.input,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            elapsed_time = time.time() - start_time
            actual_output = process.stdout
            stderr_output = process.stderr

            if process.returncode != 0:
                return SingleTestResult(
                    status=TestStatus.RUNTIME_ERROR,
                    input=test_case.input,
                    expected_output=test_case.output,
                    actual_output=actual_output,
                    error_message=stderr_output.strip() or f"Process exited with code {process.returncode}",
                    execution_time=elapsed_time
                )

            # So sánh kết quả
            norm_actual = self._normalize_output(actual_output)
            norm_expected = self._normalize_output(test_case.output)

            if norm_actual == norm_expected:
                return SingleTestResult(
                    status=TestStatus.ACCEPTED,
                    input=test_case.input,
                    expected_output=test_case.output,
                    actual_output=actual_output,
                    execution_time=elapsed_time
                )
            else:
                return SingleTestResult(
                    status=TestStatus.WRONG_ANSWER,
                    input=test_case.input,
                    expected_output=test_case.output,
                    actual_output=actual_output,
                    error_message=f"Output mismatch: Expected '{norm_expected}', got '{norm_actual}'",
                    execution_time=elapsed_time
                )

        except subprocess.TimeoutExpired:
            return SingleTestResult(
                status=TestStatus.TIME_LIMIT_EXCEEDED,
                input=test_case.input,
                expected_output=test_case.output,
                error_message=f"Execution exceeded time limit of {self.timeout}s",
                execution_time=self.timeout
            )
        except Exception as e:
            return SingleTestResult(
                status=TestStatus.RUNTIME_ERROR,
                input=test_case.input,
                expected_output=test_case.output,
                error_message=str(e),
                execution_time=time.time() - start_time
            )
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def evaluate_code(self, code: str, test_cases: List[TestCase]) -> ExecutionResult:
        """Đánh giá mã nguồn trên toàn bộ danh sách test cases."""
        if not test_cases:
            return ExecutionResult(all_passed=True, pass_rate=1.0, passed_count=0, total_count=0)

        results = []
        passed_count = 0
        first_failed = None

        for test in test_cases:
            res = self.run_single_test(code, test)
            results.append(res)
            if res.status == TestStatus.ACCEPTED:
                passed_count += 1
            elif first_failed is None:
                first_failed = res

        total_count = len(test_cases)
        pass_rate = passed_count / total_count
        all_passed = (passed_count == total_count)

        # Xây dựng verbal feedback nếu có lỗi
        verbal_feedback = ""
        if first_failed:
            verbal_feedback = (
                f"Execution Result: {first_failed.status.value}\n"
                f"Failed on Test Input:\n{first_failed.input.strip()}\n"
                f"Expected Output:\n{first_failed.expected_output.strip()}\n"
                f"Actual Output:\n{first_failed.actual_output.strip() if first_failed.actual_output else '[None]'}\n"
            )
            if first_failed.error_message:
                verbal_feedback += f"Error Details:\n{first_failed.error_message.strip()}"

        return ExecutionResult(
            all_passed=all_passed,
            pass_rate=pass_rate,
            passed_count=passed_count,
            total_count=total_count,
            first_failed_test=first_failed,
            test_results=results,
            verbal_feedback=verbal_feedback
        )
