import math
from typing import List, Optional


class MCTSNode:
    """
    Đại diện cho một nút trong cây tìm kiếm RethinkMCTS.
    Mỗi node tương ứng với một bước tư duy (Thought) hoặc chiến lược giải thuật.
    """
    def __init__(
        self,
        thought: str,
        parent: Optional['MCTSNode'] = None,
        prior_prob: float = 1.0,
        depth: int = 0
    ):
        self.thought = thought
        self.parent = parent
        self.children: List['MCTSNode'] = []
        self.depth = depth

        # Thống kê tìm kiếm MCTS
        self.visit_count: int = 0
        self.q_value: float = 0.0          # Giá trị kỳ vọng Q(s, a)
        self.prior_prob: float = prior_prob # P(a | s) từ LLM

        # Dữ liệu mã nguồn & phản hồi
        self.code: Optional[str] = None
        self.verbal_feedback: Optional[str] = None
        self.reward: float = 0.0

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def get_thought_history(self) -> List[str]:
        """Truy vết toàn bộ chuỗi tư duy từ Root đến Node hiện tại."""
        thoughts = []
        curr = self
        while curr is not None:
            if curr.thought:  # Bỏ qua root nếu rỗng
                thoughts.append(curr.thought)
            curr = curr.parent
        return list(reversed(thoughts))

    def compute_p_ucb(self, c_base: float = 10.0, c: float = 4.0) -> float:
        """
        Tính điểm P-UCB theo phương trình (1) và (2) trong bài báo RethinkMCTS:
        P-UCB(s, a) = Q(s, a) + beta(s) * P(a | s) * [sqrt(ln(N(s))) / (1 + N(s'))]
        với beta(s) = log((N(s) + c_base + 1) / c_base) + c
        """
        if self.parent is None:
            return self.q_value

        parent_visits = self.parent.visit_count
        if parent_visits == 0:
            return self.q_value + c * self.prior_prob

        beta = math.log((parent_visits + c_base + 1.0) / c_base) + c
        exploration_term = beta * self.prior_prob * (math.sqrt(math.log(parent_visits + 1e-5)) / (1.0 + self.visit_count))
        return self.q_value + exploration_term

    def update(self, reward: float):
        """Cập nhật số lần thăm và giá trị Q (lấy trung bình tích lũy)."""
        self.visit_count += 1
        self.q_value += (reward - self.q_value) / self.visit_count
        self.reward = max(self.reward, reward)
