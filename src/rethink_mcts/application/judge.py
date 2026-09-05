"""
Independent Hidden Judge application service (§11.1, §15.1).
Evaluates frozen selected candidates against hidden test suites.
"""

from dataclasses import dataclass
from typing import Optional
from rethink_mcts.domain.candidate import ProgramCandidate, ExecutionSummary
from rethink_mcts.domain.problem import HiddenProblem, ExecutionSpec, ProblemLimits
from rethink_mcts.ports.execution import PublicExecutor


@dataclass(frozen=True)
class JudgeResult:
    problem_id: str
    candidate_id: str
    code_hash: str
    all_hidden_passed: bool
    hidden_pass_rate: float
    hidden_passed: int
    hidden_total: int
    execution_summary: ExecutionSummary


class HiddenJudge:
    def __init__(self, executor: PublicExecutor):
        self.executor = executor

    def judge(
        self,
        candidate: ProgramCandidate,
        hidden_problem: HiddenProblem,
        execution_spec: Optional[ExecutionSpec] = None,
        limits: Optional[ProblemLimits] = None
    ) -> JudgeResult:
        """
        Judges a frozen candidate against the entire hidden suite.
        Does NOT alter search tree, candidate archive, or public rewards.
        """
        spec = execution_spec or ExecutionSpec()
        exec_limits = limits or ProblemLimits(
            timeout_seconds=hidden_problem.judge_spec.timeout_seconds,
            memory_mb=hidden_problem.judge_spec.memory_mb
        )

        cases = hidden_problem.hidden_suite.cases
        summary = self.executor.evaluate(
            candidate=candidate,
            tests=cases,
            spec=spec,
            limits=exec_limits
        )

        pass_rate = summary.pass_rate if summary.pass_rate is not None else 0.0

        return JudgeResult(
            problem_id=hidden_problem.problem_id,
            candidate_id=candidate.candidate_id,
            code_hash=candidate.code_hash,
            all_hidden_passed=summary.all_passed,
            hidden_pass_rate=pass_rate,
            hidden_passed=summary.passed,
            hidden_total=summary.total,
            execution_summary=summary
        )
