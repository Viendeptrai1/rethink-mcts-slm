"""
Prior normalization and deduplication policy matching §6.2 of spec.
"""

from typing import List, Tuple
from rethink_mcts.domain.errors import InvalidModelOutputError
from rethink_mcts.domain.tree import ThoughtProposal


class PriorPolicy:
    def __init__(self, fallback_mode: str = "uniform_after_retry"):
        self.fallback_mode = fallback_mode

    def process_raw_proposals(
        self,
        raw_items: List[Tuple[str, float]]
    ) -> List[ThoughtProposal]:
        """
        Processes raw (thought_text, raw_reasonableness) pairs:
        1. Strips text and ignores empty proposals.
        2. Deduplicates by normalized text, summing raw reasonableness scores (U11).
        3. Validates scores (finite, non-negative).
        4. Normalizes priors so sum(P_i) == 1.0 (U09, U10).
        """
        if not raw_items:
            raise InvalidModelOutputError("No proposals provided")

        # 1. Filter and Deduplicate
        seen_indices = {}
        unique_proposals: List[Tuple[str, float]] = []

        for text, score in raw_items:
            norm_text = " ".join(text.strip().split())
            if not norm_text:
                continue
            dedup_key = norm_text.lower()

            # Validate individual score
            if not isinstance(score, (int, float)) or score != score:  # NaN check
                score = 0.0
            if score < 0:
                score = 0.0

            if dedup_key in seen_indices:
                idx = seen_indices[dedup_key]
                prev_text, prev_score = unique_proposals[idx]
                unique_proposals[idx] = (prev_text, prev_score + float(score))
            else:
                seen_indices[dedup_key] = len(unique_proposals)
                unique_proposals.append((norm_text, float(score)))

        if not unique_proposals:
            raise InvalidModelOutputError("All proposals were empty or invalid")

        total_mass = sum(s for _, s in unique_proposals)

        # 2. Normalize or fallback
        if total_mass <= 0:
            if self.fallback_mode == "uniform_after_retry":
                uniform_p = 1.0 / len(unique_proposals)
                return [
                    ThoughtProposal(
                        text=t,
                        raw_reasonableness=s,
                        normalized_prior=uniform_p
                    )
                    for t, s in unique_proposals
                ]
            else:
                raise InvalidModelOutputError(f"Total reasonableness score is non-positive ({total_mass})")

        return [
            ThoughtProposal(
                text=t,
                raw_reasonableness=s,
                normalized_prior=s / total_mass
            )
            for t, s in unique_proposals
        ]
