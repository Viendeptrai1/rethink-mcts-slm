"""
Search termination policies following §7.6 of spec.
"""

from typing import Optional, Tuple
from rethink_mcts.domain.budget import BudgetManager
from rethink_mcts.domain.tree import Tree, NodeStatus


class StoppingPolicy:
    def __init__(self, max_depth: int = 4, early_stop_mode: str = "none"):
        self.max_depth = max_depth
        self.early_stop_mode = early_stop_mode  # "none" | "public_all_passed"

    def should_stop(
        self,
        tree: Tree,
        budget: BudgetManager,
        best_public_all_passed: bool = False
    ) -> Tuple[bool, str]:
        """
        Determines whether search should terminate and provides canonical stop reason.
        """
        exhausted, reason = budget.is_exhausted()
        if exhausted:
            return True, reason

        if self.early_stop_mode == "public_all_passed" and best_public_all_passed:
            return True, "optional_public_early_stop"

        # Check if tree has any remaining work (nodes that are UNEVALUATED or expandable READY)
        has_work = False
        for node in tree.nodes.values():
            if node.status == NodeStatus.UNEVALUATED:
                has_work = True
                break
            if node.status == NodeStatus.READY and node.depth < self.max_depth:
                has_work = True
                break

        if not has_work:
            return True, "tree_exhausted"

        return False, ""
