import logging
from typing import Tuple
from mcts.node import MCTSNode
from data.schemas import Problem, ExecutionResult
from models.client import BaseLLMClient
from sandbox.executor import CodeExecutor
from sandbox.analyzer import FeedbackAnalyzer

logger = logging.getLogger(__name__)


def perform_rethink(
    node: MCTSNode,
    problem: Problem,
    client: BaseLLMClient,
    executor: CodeExecutor,
    analyzer: FeedbackAnalyzer,
    reward_a: float = 0.8,
    reward_b: float = 0.2
) -> Tuple[str, ExecutionResult, float]:
    """
    Thực hiện cơ chế Rethink (Phương trình trong bài báo RethinkMCTS):
    1. Trích xuất phản hồi thực thi (Verbal Feedback) từ test case thất bại.
    2. Yêu cầu LLM điều chỉnh lại bước tư duy bị lỗi tại nút lá: z_new ~ p(z | s, f, z_old).
    3. Sinh lại mã nguồn mới dựa trên tư duy đã sửa đổi: C_new ~ p(C | s, z_new).
    4. Chạy lại kiểm thử tự động trong sandbox để tính toán lại điểm thưởng.
    """
    if not node.code or not node.verbal_feedback:
        return "", ExecutionResult(), 0.0

    history = node.get_thought_history()
    previous_thoughts = history[:-1] if len(history) > 1 else []
    erroneous_thought = node.thought

    logger.info(f"[Rethink] Kích hoạt cơ chế Rethink cho nút lỗi: '{erroneous_thought[:60]}...'")

    # 1. Sinh tư duy mới thay thế
    new_thought = client.rethink_thought(
        problem_desc=problem.description,
        previous_thoughts=previous_thoughts,
        erroneous_thought=erroneous_thought,
        code=node.code,
        feedback=node.verbal_feedback
    )
    node.thought = new_thought

    # 2. Sinh lại mã nguồn
    updated_history = node.get_thought_history()
    new_code = client.generate_code(problem.description, updated_history)
    node.code = new_code

    # 3. Đánh giá lại trên public tests
    exec_result = executor.evaluate_code(new_code, problem.public_tests)

    # 4. Tính lại reward
    v_test = exec_result.pass_rate
    if v_test == 1.0:
        v_llm = client.self_evaluate(problem.description, new_code)
        reward = reward_a * v_test + reward_b * v_llm
    else:
        reward = v_test

    node.reward = max(node.reward, reward)
    node.verbal_feedback = analyzer.format_rethink_feedback(problem.title, new_code, exec_result)

    logger.info(f"[Rethink Hoàn tất] Tư duy mới: '{new_thought[:60]}...' | Điểm thưởng mới: {reward:.3f}")
    return new_code, exec_result, reward
