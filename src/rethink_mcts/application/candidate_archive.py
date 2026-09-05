"""
Immutable candidate archive and lookup.
"""

from typing import Dict, List, Optional, Tuple
from rethink_mcts.domain.candidate import ProgramCandidate, EvaluationRecord


class CandidateArchive:
    def __init__(self):
        self._entries: List[Tuple[ProgramCandidate, EvaluationRecord]] = []
        self._by_candidate_id: Dict[str, Tuple[ProgramCandidate, EvaluationRecord]] = {}
        self._unique_code_hashes: set[str] = set()

    @property
    def entries(self) -> List[Tuple[ProgramCandidate, EvaluationRecord]]:
        return list(self._entries)

    @property
    def unique_programs_count(self) -> int:
        return len(self._unique_code_hashes)

    def add(self, candidate: ProgramCandidate, evaluation: EvaluationRecord) -> None:
        pair = (candidate, evaluation)
        self._entries.append(pair)
        self._by_candidate_id[candidate.candidate_id] = pair
        self._unique_code_hashes.add(candidate.code_hash)

    def get_by_id(self, candidate_id: str) -> Optional[Tuple[ProgramCandidate, EvaluationRecord]]:
        return self._by_candidate_id.get(candidate_id)

    def get_best(self) -> Optional[Tuple[ProgramCandidate, EvaluationRecord]]:
        valid = [pair for pair in self._entries if pair[1].reward is not None]
        if not valid:
            return None
        return max(valid, key=lambda p: (p[1].reward, -p[0].created_sequence))
