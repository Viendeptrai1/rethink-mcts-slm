"""
Storage and caching ports for search persistence.
"""

from typing import Optional, Protocol, runtime_checkable
from rethink_mcts.domain.candidate import ProgramCandidate, EvaluationRecord, ExecutionSummary
from rethink_mcts.domain.events import EventEnvelope
from rethink_mcts.domain.tree import Tree
from rethink_mcts.domain.budget import Usage


@runtime_checkable
class EvaluationCache(Protocol):
    """Caches sandbox execution results by exact execution fingerprint."""
    def get(self, cache_key: str) -> Optional[ExecutionSummary]:
        ...

    def put(self, cache_key: str, summary: ExecutionSummary) -> None:
        ...


@runtime_checkable
class RunStore(Protocol):
    """Durable persistence for artifacts, event logs, checkpoints, and reports."""
    def append_event(self, event: EventEnvelope) -> None:
        ...

    def save_candidate(self, candidate: ProgramCandidate) -> None:
        ...

    def save_evaluation(self, evaluation: EvaluationRecord) -> None:
        ...

    def save_checkpoint(self, problem_id: str, tree: Tree, selected_candidate_id: Optional[str]) -> None:
        ...

    def save_selected_candidate(self, problem_id: str, candidate: ProgramCandidate) -> None:
        ...

    def save_usage(self, usage: Usage) -> None:
        ...
