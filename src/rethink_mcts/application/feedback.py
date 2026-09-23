"""
Verbal feedback builder coordinating execution facts, bytecode CFG trace, and block analysis.
"""

import uuid
from typing import Optional
from rethink_mcts.domain.candidate import ProgramCandidate, EvaluationRecord
from rethink_mcts.domain.problem import PublicProblem, StdinCase, FunctionCase
from rethink_mcts.domain.feedback import (
    ExecutionFacts,
    TraceResult,
    BlockAnalysis,
    VerbalFeedback
)
from rethink_mcts.ports.execution import TraceCollector
from rethink_mcts.ports.models import BlockAnalyzer


class FeedbackService:
    def __init__(
        self,
        mode: str = "block",  # "block" | "facts_only" | "none"
        trace_collector: Optional[TraceCollector] = None,
        block_analyzer: Optional[BlockAnalyzer] = None
    ):
        self.mode = mode
        self.trace_collector = trace_collector
        self.block_analyzer = block_analyzer

    def build_feedback(
        self,
        candidate: ProgramCandidate,
        evaluation: EvaluationRecord,
        problem: PublicProblem
    ) -> VerbalFeedback:
        feedback_id = f"fb_{uuid.uuid4().hex[:10]}"
        failed_res = evaluation.execution_summary.first_failed_case

        if not failed_res:
            facts = ExecutionFacts(
                failure_kind="NONE",
                input_snippet="<none>",
                expected_output_snippet="<none>",
                actual_output_snippet="<none>",
                public_passed=evaluation.execution_summary.passed,
                public_total=evaluation.execution_summary.total
            )
            return VerbalFeedback(feedback_id=feedback_id, candidate_id=candidate.candidate_id, facts=facts)

        # Match failed test case from problem.public_tests
        failed_case = next(
            (c for c in problem.public_tests if getattr(c, "case_id", "") == failed_res.case_id),
            problem.public_tests[0] if problem.public_tests else None
        )

        input_str = ""
        expected_str = ""
        if isinstance(failed_case, StdinCase):
            input_str = failed_case.stdin.strip()
            expected_str = failed_case.expected_stdout.strip()
        elif isinstance(failed_case, FunctionCase):
            input_str = f"args={failed_case.args}, kwargs={dict(failed_case.kwargs)}"
            expected_str = str(failed_case.expected)

        facts = ExecutionFacts(
            failure_kind=failed_res.status.value,
            input_snippet=input_str[:500],
            expected_output_snippet=expected_str[:500],
            actual_output_snippet=(failed_res.actual_output or "")[:500],
            traceback_snippet=(failed_res.error_message or "")[:1000],
            public_passed=evaluation.execution_summary.passed,
            public_total=evaluation.execution_summary.total
        )

        trace_result: Optional[TraceResult] = None
        analysis: Optional[BlockAnalysis] = None

        if self.mode == "block" and self.trace_collector and failed_case:
            if failed_res.status.value == "TLE":
                trace_result = TraceResult(
                    status="timeout",
                    degraded_reason="Candidate execution timed out (TLE); skipping dynamic tracing."
                )
            else:
                try:
                    trace_result = self.trace_collector.collect_trace(
                        candidate=candidate,
                        failed_case=failed_case,
                        spec=problem.execution_spec
                    )
                except Exception as e:
                    trace_result = TraceResult(status="degraded", degraded_reason=str(e))

            if self.block_analyzer and trace_result and trace_result.status == "success":
                try:
                    analysis = self.block_analyzer.analyze(
                        statement=problem.statement,
                        candidate_code=candidate.code,
                        facts=facts,
                        trace=trace_result
                    )
                except Exception:
                    analysis = None

        return VerbalFeedback(
            feedback_id=feedback_id,
            candidate_id=candidate.candidate_id,
            facts=facts,
            trace=trace_result,
            analysis=analysis
        )
