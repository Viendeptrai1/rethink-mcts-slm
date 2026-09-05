"""
Dataset source ports separating public problem exploration from hidden evaluation.
"""

from typing import Protocol, runtime_checkable
from rethink_mcts.domain.problem import PublicProblem, HiddenProblem, HiddenSuite


@runtime_checkable
class PublicProblemSource(Protocol):
    """Source providing public problem specifications without access to hidden suites."""
    def get_problem(self, problem_id: str) -> PublicProblem:
        ...

    def list_problem_ids(self) -> tuple[str, ...]:
        ...


@runtime_checkable
class HiddenSuiteSource(Protocol):
    """Source providing hidden suites strictly for the independent Judge process."""
    def get_hidden_problem(self, problem_id: str) -> HiddenProblem:
        ...
