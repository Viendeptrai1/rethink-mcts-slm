"""
Verbal feedback builder coordinating execution facts, bytecode CFG trace, and block analysis.
"""

import uuid
import logging
from typing import Optional
from dataclasses import asdict
from rethink_mcts.application.model_calls import invoke_model
from rethink_mcts.policies.feedback import FeedbackObservation, select_feedback
from rethink_mcts.domain.errors import BudgetExceededError
from rethink_mcts.domain.candidate import ProgramCandidate, EvaluationRecord
from rethink_mcts.domain.problem import PublicProblem, StdinCase, FunctionCase, AssertionSuite
from rethink_mcts.domain.feedback import (
    ExecutionFacts,
    TraceResult,
    BlockAnalysis,
    VerbalFeedback
)
from rethink_mcts.ports.execution import TraceCollector
from rethink_mcts.ports.models import BlockAnalyzer

logger = logging.getLogger(__name__)


class FeedbackService:
    def __init__(
        self,
        mode: str = "block",  # "block" | "facts_only" | "none"
        trace_collector: Optional[TraceCollector] = None,
        block_analyzer: Optional[BlockAnalyzer] = None,
        escalate_after: int = 1, trace_timeout_seconds: float = 5.0,
        max_prompt_blocks: int = 32, max_text_chars: int = 8192
    ):
        self.mode = mode
        self.trace_collector = trace_collector
        self.block_analyzer = block_analyzer
        self.escalate_after = escalate_after
        self.trace_timeout_seconds = trace_timeout_seconds
        self.max_prompt_blocks = max_prompt_blocks
        self.max_text_chars = max_text_chars
        self.reset()

    def reset(self):
        self.observations = {}
        self.records = []

    def inherit(self, parent_node_id, child_node_id):
        self.observations[child_node_id] = list(self.observations.get(parent_node_id, ()))

    def build_feedback(
        self,
        candidate: ProgramCandidate,
        evaluation: EvaluationRecord,
        problem: PublicProblem, budget=None, reserved_model_calls=0
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

        if isinstance(failed_case, AssertionSuite):
            facts = ExecutionFacts(
                failure_kind=failed_res.status.value,
                input_snippet=failed_case.test_code[:1000],
                expected_output_snippet="Assertion suite completes successfully",
                actual_output_snippet=(failed_res.actual_output or "")[:500],
                traceback_snippet=(failed_res.error_message or "")[:1000],
                public_passed=evaluation.execution_summary.passed,
                public_total=evaluation.execution_summary.total)

        key = candidate.node_id or problem.problem_id
        previous = self.observations.setdefault(key, [])
        observation = FeedbackObservation(facts.failure_kind, evaluation.v_test or 0.0, candidate.code_hash)
        decision = select_feedback(self.mode, observation, previous, self.escalate_after)
        previous.append(observation)
        level, reason = decision.level, decision.reason
        trace_result: Optional[TraceResult] = None
        analysis: Optional[BlockAnalysis] = None

        if level in ("trace", "block") and self.trace_collector and failed_case:
            if failed_res.status.value == "TLE":
                trace_result = TraceResult(
                    status="timeout",
                    degraded_reason="Candidate execution timed out (TLE); skipping dynamic tracing."
                )
            else:
                try:
                    if budget:
                        budget.reserve_sandbox_runs(1)
                        budget.record_trace_run()
                    trace_result = self.trace_collector.collect_trace(
                        candidate=candidate,
                        failed_case=failed_case,
                        spec=problem.execution_spec,
                        timeout_seconds=min(self.trace_timeout_seconds, budget.remaining_seconds()) if budget else self.trace_timeout_seconds
                    )
                except Exception as e:
                    trace_result = TraceResult(status="degraded", degraded_reason=str(e))

            if level == "block" and self.block_analyzer and trace_result and trace_result.status == "success":
                try:
                    if budget and not budget.can_call_model(1 + reserved_model_calls):
                        logger.info("Budget limit: cannot call block analyzer (need 1 + %d reserved calls)", reserved_model_calls)
                        raise BudgetExceededError("Reserved regeneration calls take priority")
                    if budget:
                        analysis = invoke_model(budget, self.block_analyzer, "analyze", "block_analysis",
                            statement=problem.statement, candidate_code=candidate.code, facts=facts, trace=trace_result)
                    else:
                        analysis = self.block_analyzer.analyze(
                            statement=problem.statement,
                            candidate_code=candidate.code,
                            facts=facts,
                            trace=trace_result
                        )
                    if analysis and analysis.assessments:
                        logger.info("Block analysis succeeded with %d assessments", len(analysis.assessments))
                except Exception as exc:
                    logger.warning("Block analysis skipped/failed: %s", exc)
                    analysis = None

        effective = level
        if level in ("trace", "block") and (not trace_result or trace_result.status != "success"):
            effective, reason = "facts_only", reason + ":trace_unavailable"
            logger.info("Feedback downgraded to %s: trace unavailable (%s)", effective, trace_result.degraded_reason if trace_result else "no trace")
        elif level == "block" and analysis is None:
            effective, reason = "trace", reason + ":analysis_unavailable_or_budget"
            logger.info("Feedback downgraded to %s: analysis unavailable or budget reservation", effective)
        feedback = VerbalFeedback(
            feedback_id=feedback_id, candidate_id=candidate.candidate_id,
            facts=facts, trace=trace_result, analysis=analysis, level=effective,
            decision_reason=reason, max_prompt_blocks=self.max_prompt_blocks,
            max_text_chars=self.max_text_chars)
        self.records.append({"requested_level": level, "stagnation": decision.stagnation,
                             "feedback": asdict(feedback)})
        return feedback
