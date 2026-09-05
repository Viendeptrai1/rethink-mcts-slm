"""
Unit tests for HiddenJudge and U18: Hidden test suite absence / partial evaluation.
"""

from rethink_mcts.domain.candidate import ProgramCandidate, ExecutionSummary
from rethink_mcts.domain.problem import HiddenProblem, HiddenSuite, JudgeSpec, StdinCase
from rethink_mcts.adapters.execution.trusted_fixture_executor import TrustedFixtureExecutor
from rethink_mcts.application.judge import HiddenJudge


def test_u18_hidden_suite_empty_returns_incomplete_or_zero():
    """
    U18: Hidden không có, hoặc partial evaluation -> N/A/incomplete, không giả AC.
    """
    candidate = ProgramCandidate("c1", "p1", "print('hello')", "h1")
    empty_hidden = HiddenProblem("p1", hidden_suite=HiddenSuite(cases=()), judge_spec=JudgeSpec())

    executor = TrustedFixtureExecutor()
    judge = HiddenJudge(executor=executor)
    res = judge.judge(candidate, empty_hidden)

    assert res.all_hidden_passed is False
    assert res.hidden_total == 0
    assert res.hidden_passed == 0
    assert res.hidden_pass_rate == 0.0
    assert res.execution_summary.pass_rate is None
