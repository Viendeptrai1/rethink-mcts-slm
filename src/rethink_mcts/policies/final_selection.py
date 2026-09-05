"""
Final candidate selection policy following §6.5 of spec.
"""

from typing import List, Optional, Tuple
from rethink_mcts.domain.candidate import ProgramCandidate, EvaluationRecord


class FinalSelectionPolicy:
    def __init__(self, mode: str = "max_reward"):
        self.mode = mode  # "max_reward" | "public_first_then_reward"

    def select(
        self,
        archive: List[Tuple[ProgramCandidate, EvaluationRecord]]
    ) -> Optional[ProgramCandidate]:
        """
        Selects the best candidate program from the entire search history archive.
        Returns None if archive is empty or no valid evaluations exist.
        """
        valid_pairs = [
            (c, e) for c, e in archive
            if e.reward is not None
        ]
        if not valid_pairs:
            return None

        if self.mode == "public_first_then_reward":
            # U13 ablation: prioritize candidates that passed all public tests
            full_pass_pairs = [
                (c, e) for c, e in valid_pairs
                if e.execution_summary.all_passed
            ]
            if full_pass_pairs:
                valid_pairs = full_pass_pairs

        # Default / Reference mode: max_reward across entire archive (U12, U13)
        # Tie break by creation order (lower created_sequence)
        best_candidate, _ = max(
            valid_pairs,
            key=lambda pair: (pair[1].reward, -pair[0].created_sequence)
        )
        return best_candidate
