"""
Acceptance test Scenario A: Watermelon full pipeline provenance (§18.3).
"""

import json
from rethink_mcts.domain.problem import (
    PublicProblem,
    HiddenProblem,
    HiddenSuite,
    StdinCase,
    ExecutionSpec,
    ProblemLimits,
    PublicMetadata,
    JudgeSpec
)
from rethink_mcts.domain.budget import BudgetLimits
from rethink_mcts.policies.selection import PUCBSelector
from rethink_mcts.policies.prior import PriorPolicy
from rethink_mcts.policies.backup import MaxBackupPolicy
from rethink_mcts.policies.reward import PaperDualRewardPolicy
from rethink_mcts.policies.stopping import StoppingPolicy
from rethink_mcts.policies.final_selection import FinalSelectionPolicy
from rethink_mcts.adapters.llm.mock import ScenarioMockLLM
from rethink_mcts.adapters.execution.trusted_fixture_executor import TrustedFixtureExecutor
from rethink_mcts.application.evaluate import CandidateEvaluator
from rethink_mcts.application.feedback import FeedbackService
from rethink_mcts.application.search import SearchEngine
from rethink_mcts.domain.candidate import CandidateOrigin


def load_fixtures():
    with open("tests/fixtures/watermelon_public.json", "r") as f:
        pub_raw = json.load(f)
    with open("tests/fixtures/watermelon_hidden.json", "r") as f:
        hid_raw = json.load(f)

    public_tests = tuple(
        StdinCase(stdin=c["stdin"], expected_stdout=c["expected_stdout"], case_id=c["case_id"])
        for c in pub_raw["public_tests"]
    )
    public_problem = PublicProblem(
        problem_id=pub_raw["problem_id"],
        statement=pub_raw["statement"],
        execution_spec=ExecutionSpec(),
        public_tests=public_tests,
        limits=ProblemLimits(),
        metadata=PublicMetadata(source=pub_raw["metadata"]["source"])
    )

    hidden_cases = tuple(
        StdinCase(stdin=c["stdin"], expected_stdout=c["expected_stdout"], case_id=c["case_id"])
        for c in hid_raw["hidden_suite"]["cases"]
    )
    hidden_problem = HiddenProblem(
        problem_id=hid_raw["problem_id"],
        hidden_suite=HiddenSuite(cases=hidden_cases),
        judge_spec=JudgeSpec()
    )
    return public_problem, hidden_problem


def test_scenario_a_watermelon_provenance():
    public_problem, hidden_problem = load_fixtures()

    # 1. Setup mock, executor, policies
    mock_llm = ScenarioMockLLM(default_critic_score=0.9)
    executor = TrustedFixtureExecutor()
    reward_policy = PaperDualRewardPolicy(test_weight=0.8, llm_weight=0.2, critic_min=0.0, critic_max=1.0)
    budget_limits = BudgetLimits(max_code_generations=4, max_model_calls=20, max_search_iterations=10)

    evaluator = CandidateEvaluator(
        executor=executor,
        critic=mock_llm,
        reward_policy=reward_policy
    )
    feedback_service = FeedbackService(mode="block", trace_collector=None, block_analyzer=mock_llm)

    engine = SearchEngine(
        proposer=mock_llm,
        generator=mock_llm,
        refiner=mock_llm,
        evaluator=evaluator,
        feedback_service=feedback_service,
        selector=PUCBSelector(c_base=10.0, c=4.0),
        backup_policy=MaxBackupPolicy(),
        stopping_policy=StoppingPolicy(max_depth=3),
        final_selector=FinalSelectionPolicy(mode="max_reward"),
        budget_limits=budget_limits,
        width=2,
        max_depth=3,
        max_rethinks_per_node=1
    )

    # 2. Solve problem
    result = engine.solve(public_problem)

    # 3. Assertions
    assert result.selected_candidate is not None
    assert "w > 2" in result.selected_candidate.code

    # Archive holds initial candidate and rethink candidate
    entries = result.archive.entries
    assert len(entries) >= 2

    initial_candidates = [c for c, e in entries if c.origin == CandidateOrigin.INITIAL]
    rethink_candidates = [c for c, e in entries if c.origin == CandidateOrigin.RETHINK]
    assert len(initial_candidates) >= 1
    assert len(rethink_candidates) >= 1

    # Check that initial candidate failed w=2 (pass_rate 0.5)
    first_eval = entries[0][1]
    assert first_eval.v_test == 0.5
    assert first_eval.execution_summary.all_passed is False

    # Check that rethink candidate passed public tests (pass_rate 1.0) and got critic score
    rethink_eval = next(e for c, e in entries if c.origin == CandidateOrigin.RETHINK)
    assert rethink_eval.v_test == 1.0
    assert rethink_eval.execution_summary.all_passed is True
    # Reward = 0.8 * 1.0 + 0.2 * 0.9 = 0.98
    assert abs(rethink_eval.reward - 0.98) < 1e-12

    # 4. Independent Judge on Hidden Suite
    judge_summary = executor.evaluate(
        candidate=result.selected_candidate,
        tests=hidden_problem.hidden_suite.cases,
        spec=public_problem.execution_spec,
        limits=public_problem.limits
    )
    assert judge_summary.all_passed is True
    assert judge_summary.passed == len(hidden_problem.hidden_suite.cases)
    assert judge_summary.pass_rate == 1.0
