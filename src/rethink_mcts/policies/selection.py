"""
P-UCB Selection policy following Paper Eq. 1-2 with bootstrap/tie resolutions.
"""

import math
from typing import Optional
from rethink_mcts.domain.tree import SearchNode, NodeStatus, Tree


class PUCBSelector:
    """
    Selects children nodes based on P-UCB score:
    P_UCB(s, a) = Q(s, a) + beta(s) * P(a|s) * [sqrt(ln(N(s))) / (1 + N(s'))]
    beta(s) = ln((N(s) + c_base + 1) / c_base) + c
    """
    def __init__(self, c_base: float = 10.0, c: float = 4.0):
        self.c_base = c_base
        self.c = c

    def compute_score(
        self,
        parent_visits: int,
        child_visits: int,
        prior: float,
        q_value: float
    ) -> float:
        """
        Pure formula computation matching U01.
        """
        if parent_visits <= 0:
            # Bootstrap guard: parent has 0 visits
            return q_value + self.c * prior

        beta = math.log((parent_visits + self.c_base + 1.0) / self.c_base) + self.c
        exploration = beta * prior * (math.sqrt(math.log(parent_visits)) / (1.0 + child_visits))
        return q_value + exploration

    def select_best_child(self, tree: Tree, parent_node: SearchNode) -> Optional[SearchNode]:
        """
        Selects the best child among valid non-exhausted children according to §6.3:
        1. If there are unvisited (visits == 0) and UNEVALUATED or READY children,
           pick the one with the highest prior, tie-broken by creation order.
        2. If all valid children have visits >= 1, use exact P-UCB formula.
        3. Skip CLOSED children.
        """
        eligible_children = [
            tree.nodes[cid] for cid in parent_node.child_ids
            if tree.nodes[cid].status != NodeStatus.CLOSED
        ]
        if not eligible_children:
            return None

        # Check for unvisited eligible children
        unvisited = [ch for ch in eligible_children if ch.visits == 0]
        if unvisited:
            # Prioritize unvisited by highest prior, then original order (U02)
            return max(unvisited, key=lambda ch: ch.prior)

        # All eligible have visits >= 1. Parent must have visits >= 1.
        best_child = None
        best_score = -float("inf")

        for ch in eligible_children:
            score = self.compute_score(
                parent_visits=parent_node.visits,
                child_visits=ch.visits,
                prior=ch.prior,
                q_value=ch.q_max
            )
            # Tie breaking: score > best_score, then higher prior
            if score > best_score:
                best_score = score
                best_child = ch
            elif abs(score - best_score) < 1e-14 and best_child is not None:
                if ch.prior > best_child.prior:
                    best_score = score
                    best_child = ch

        return best_child
