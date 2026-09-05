from data.schemas import ExecutionResult, TestStatus


class FeedbackAnalyzer:
    """
    Phân tích kết quả thực thi và cấu trúc hóa 'Verbal Feedback' chi tiết
    để cung cấp ngữ cảnh sửa lỗi cho cơ chế Rethink của MCTS.
    """
    @staticmethod
    def format_rethink_feedback(problem_title: str, code: str, execution_result: ExecutionResult) -> str:
        """Tạo chuỗi feedback chuẩn hoá cho prompt Rethink."""
        if execution_result.all_passed:
            return "All test cases passed."

        failed = execution_result.first_failed_test
        if not failed:
            return "Code execution failed with unknown error."

        feedback_parts = [
            f"[TEST EXECUTION REPORT for '{problem_title}']",
            f"Pass Rate: {execution_result.passed_count}/{execution_result.total_count} ({execution_result.pass_rate*100:.1f}%)",
            f"Failure Type: {failed.status.value}",
            f"--- Failed Input ---\n{failed.input.strip()}",
            f"--- Expected Output ---\n{failed.expected_output.strip()}",
            f"--- Actual Output ---\n{failed.actual_output.strip() if failed.actual_output else '[Empty / None]'}"
        ]

        if failed.error_message:
            feedback_parts.append(f"--- Traceback / Diagnostics ---\n{failed.error_message.strip()}")

        if failed.status == TestStatus.TIME_LIMIT_EXCEEDED:
            feedback_parts.append("Diagnosis Hint: The solution is too slow or contains an infinite loop. Consider optimizing time complexity (e.g. from O(N^2) to O(N log N) or O(N)).")
        elif failed.status == TestStatus.WRONG_ANSWER:
            feedback_parts.append("Diagnosis Hint: Logic mismatch on edge cases or boundary conditions (e.g., n=0, n=1, negative numbers, or strict even/odd constraints).")
        elif failed.status == TestStatus.RUNTIME_ERROR:
            feedback_parts.append("Diagnosis Hint: Runtime Exception encountered (e.g., IndexError, ZeroDivisionError, ValueError). Ensure inputs are parsed correctly according to the problem constraints.")

        return "\n\n".join(feedback_parts)
