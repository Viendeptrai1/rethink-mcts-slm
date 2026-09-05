"""
Execution sandbox and trace collection ports.
"""

from typing import Protocol, runtime_checkable
from rethink_mcts.domain.candidate import ProgramCandidate, ExecutionSummary
from rethink_mcts.domain.problem import TestCase, ExecutionSpec, ProblemLimits
from rethink_mcts.domain.feedback import TraceResult


@runtime_checkable
class PublicExecutor(Protocol):
    """Executes candidate code against test cases in an isolated environment."""
    def evaluate(
        self,
        candidate: ProgramCandidate,
        tests: tuple[TestCase, ...],
        spec: ExecutionSpec,
        limits: ProblemLimits
    ) -> ExecutionSummary:
        ...


@runtime_checkable
class TraceCollector(Protocol):
    """Collects runtime basic-block visits and variable snapshots on a failed test case."""
    def collect_trace(
        self,
        candidate: ProgramCandidate,
        failed_case: TestCase,
        spec: ExecutionSpec,
        timeout_seconds: float = 5.0
    ) -> TraceResult:
        ...
