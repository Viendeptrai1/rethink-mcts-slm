"""
MaxBackup policy following §6.5 of RethinkMCTS spec.
"""

from typing import Set
from rethink_mcts.domain.tree import Tree


class MaxBackupPolicy:
    """
    Backpropagates reward using max value update:
    N <- N + 1
    Q <- max(Q, r)
    Guaranteed idempotent by evaluation_id tracking.
    """
    def __init__(self):
        self._committed_evaluations: Set[str] = set()

    def backup(
        self,
        tree: Tree,
        leaf_node_id: str,
        reward: float,
        evaluation_id: str
    ) -> bool:
        """
        Backpropagates reward from leaf_node_id to root.
        Returns True if newly committed, False if already committed (idempotent).
        """
        if evaluation_id in self._committed_evaluations:
            return False

        curr_id = leaf_node_id
        while curr_id is not None:
            node = tree.nodes[curr_id]
            node.visits += 1
            node.q_max = max(node.q_max, reward)
            node.latest_evaluation_id = evaluation_id
            curr_id = node.parent_id

        self._committed_evaluations.add(evaluation_id)
        return True
