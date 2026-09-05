import logging
from typing import Dict, Tuple, Optional
from mcts.node import MCTSNode
from mcts.rethink import perform_rethink
from data.schemas import Problem
from models.client import BaseLLMClient
from sandbox.executor import CodeExecutor
from sandbox.analyzer import FeedbackAnalyzer

logger = logging.getLogger(__name__)


class RethinkMCTSEngine:
    """
    Động cơ tìm kiếm Monte Carlo Tree Search kết hợp cơ chế Rethink
    cho bài toán sinh mã nguồn (Dựa trên paper RethinkMCTS).
    """
    def __init__(
        self,
        client: BaseLLMClient,
        executor: CodeExecutor,
        analyzer: FeedbackAnalyzer,
        max_rollouts: int = 4,
        max_children: int = 3,
        c_base: float = 10.0,
        c: float = 4.0,
        reward_a: float = 0.8,
        reward_b: float = 0.2
    ):
        self.client = client
        self.executor = executor
        self.analyzer = analyzer
        self.max_rollouts = max_rollouts
        self.max_children = max_children
        self.c_base = c_base
        self.c = c
        self.reward_a = reward_a
        self.reward_b = reward_b

    def search(self, problem: Problem) -> Tuple[str, float, Dict[str, float], MCTSNode]:
        """
        Thực hiện toàn bộ quy trình tìm kiếm MCTS trên cây tư duy cho một bài toán.
        Trả về: (mã nguồn tốt nhất, điểm thưởng cao nhất, từ điển {code: reward}, root node)
        """
        root = MCTSNode(thought="", parent=None, depth=0)
        program_dict: Dict[str, float] = {}

        logger.info(f"Bắt đầu RethinkMCTS cho bài toán '{problem.title}' (Max rollouts={self.max_rollouts})")

        for rollout_idx in range(1, self.max_rollouts + 1):
            logger.info(f"\n--- [Rollout {rollout_idx}/{self.max_rollouts}] ---")
            node = root

            # 1. Giai đoạn Selection (Lựa chọn dựa trên P-UCB)
            while not node.is_leaf():
                best_child = max(node.children, key=lambda ch: ch.compute_p_ucb(self.c_base, self.c))
                node = best_child
                logger.debug(f"Selection -> Chọn node ở depth {node.depth} với P-UCB={node.compute_p_ucb(self.c_base, self.c):.3f}")

            # 2. Giai đoạn Expansion (Mở rộng nhánh tư duy)
            current_history = node.get_thought_history()
            new_thoughts = self.client.generate_thoughts(
                problem_desc=problem.description,
                previous_thoughts=current_history,
                k=self.max_children
            )

            for th in new_thoughts:
                child = MCTSNode(
                    thought=th,
                    parent=node,
                    prior_prob=1.0 / max(1, len(new_thoughts)),
                    depth=node.depth + 1
                )
                node.children.append(child)

            # Chọn nhánh con đầu tiên để đánh giá
            eval_node = node.children[0] if node.children else node

            # 3. Giai đoạn Evaluation (Sinh mã và Chạy Sandbox)
            eval_history = eval_node.get_thought_history()
            code = self.client.generate_code(problem.description, eval_history)
            eval_node.code = code

            exec_res = self.executor.evaluate_code(code, problem.public_tests)
            v_test = exec_res.pass_rate

            if v_test == 1.0:
                v_llm = self.client.self_evaluate(problem.description, code)
                reward = self.reward_a * v_test + self.reward_b * v_llm
            else:
                reward = v_test

            eval_node.reward = reward
            eval_node.verbal_feedback = self.analyzer.format_rethink_feedback(problem.title, code, exec_res)
            program_dict[code] = reward
            logger.info(f"Evaluation -> Pass rate public: {exec_res.passed_count}/{exec_res.total_count} | Reward ban đầu: {reward:.3f}")

            # 4. Giai đoạn Backpropagation (Lan truyền ngược)
            curr = eval_node
            while curr is not None:
                curr.update(reward)
                curr = curr.parent

            # 5. Giai đoạn Rethink (Nếu chưa qua hết public tests)
            if v_test < 1.0:
                re_code, re_exec, re_reward = perform_rethink(
                    node=eval_node,
                    problem=problem,
                    client=self.client,
                    executor=self.executor,
                    analyzer=self.analyzer,
                    reward_a=self.reward_a,
                    reward_b=self.reward_b
                )
                if re_code:
                    program_dict[re_code] = re_reward
                    # Cập nhật ngược lại nếu điểm sau khi rethink tốt hơn
                    if re_reward > reward:
                        curr = eval_node
                        while curr is not None:
                            curr.reward = max(curr.reward, re_reward)
                            curr = curr.parent

            # Kiểm tra nếu đã tìm ra code đạt điểm tối đa (1.0 hoặc hoàn hảo)
            if program_dict and max(program_dict.values()) >= 1.0:
                logger.info(f"[Sớm hội tụ] Đã tìm thấy mã nguồn hoàn hảo tại rollout {rollout_idx}!")
                break

        # Trả về code có điểm thưởng cao nhất
        if not program_dict:
            return "", 0.0, {}, root

        best_code = max(program_dict, key=program_dict.get)
        best_reward = program_dict[best_code]
        logger.info(f"Tìm kiếm hoàn tất! Reward tốt nhất: {best_reward:.3f}")
        return best_code, best_reward, program_dict, root
