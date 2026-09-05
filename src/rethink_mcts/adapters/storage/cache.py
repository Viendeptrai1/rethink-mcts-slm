"""
Execution result caching implementing EvaluationCache port (§13.1).
"""

import hashlib
from typing import Dict, Optional
from rethink_mcts.domain.candidate import ExecutionSummary
from rethink_mcts.ports.storage import EvaluationCache


class InMemoryEvaluationCache(EvaluationCache):
    def __init__(self):
        self._cache: Dict[str, ExecutionSummary] = {}

    @staticmethod
    def compute_key(code_hash: str, suite_hash: str, limits_str: str) -> str:
        raw = f"{code_hash}:{suite_hash}:{limits_str}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def get(self, cache_key: str) -> Optional[ExecutionSummary]:
        return self._cache.get(cache_key)

    def put(self, cache_key: str, summary: ExecutionSummary) -> None:
        self._cache[cache_key] = summary
