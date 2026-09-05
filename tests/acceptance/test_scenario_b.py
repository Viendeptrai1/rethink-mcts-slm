"""
Acceptance test Scenario B: Anti-oracle verification (§18.4).
Verifies that when multiple candidates pass public tests, the final candidate is selected
solely based on search reward without looking at hidden tests.
If selected candidate fails hidden tests, final Pass@1 is 0.
"""

from rethink_mcts.domain.candidate import ProgramCandidate, EvaluationRecord, ExecutionSummary
from rethink_mcts.domain.problem import StdinCase, HiddenProblem, HiddenSuite, JudgeSpec, ExecutionSpec, ProblemLimits
from rethink_mcts.policies.final_selection import FinalSelectionPolicy
from rethink_mcts.adapters.execution.trusted_fixture_executor import TrustedFixtureExecutor


def test_scenario_b_anti_oracle_hidden_fail():
    # Candidate A: passes public, critic gave 0.95 -> total reward = 0.8*1 + 0.2*0.95 = 0.99
    # But Candidate A hardcodes public outputs (fails on hidden test 3)
    code_a = """w = int(input())
if w == 8:
    print('YES')
elif w == 2:
    print('NO')
else:
    print('YES')  # Bug: prints YES for 3!
"""
    c_a = ProgramCandidate("cand_A", "prob_b", code_a, "hash_a", created_sequence=1)
    e_a = EvaluationRecord(
        evaluation_id="eval_a",
        candidate_id="cand_A",
        v_test=1.0,
        reward=0.99,
        execution_summary=ExecutionSummary(2, 2, 2, 0, 1.0, True)
    )

    # Candidate B: passes public, critic gave 0.80 -> total reward = 0.8*1 + 0.2*0.80 = 0.96
    # Candidate B is actually general and correct on all hidden tests
    code_b = """w = int(input())
if w % 2 == 0 and w > 2:
    print('YES')
else:
    print('NO')
"""
    c_b = ProgramCandidate("cand_B", "prob_b", code_b, "hash_b", created_sequence=2)
    e_b = EvaluationRecord(
        evaluation_id="eval_b",
        candidate_id="cand_B",
        v_test=1.0,
        reward=0.96,
        execution_summary=ExecutionSummary(2, 2, 2, 0, 1.0, True)
    )

    # Final selection strictly follows max_reward without oracle access to hidden suite
    selector = FinalSelectionPolicy(mode="max_reward")
    selected = selector.select([(c_a, e_a), (c_b, e_b)])
    assert selected is not None
    assert selected.candidate_id == "cand_A"

    # Now evaluate selected candidate against hidden suite
    hidden_suite = HiddenSuite(
        cases=(
            StdinCase(stdin="3\n", expected_stdout="NO\n", case_id="h1"),
            StdinCase(stdin="4\n", expected_stdout="YES\n", case_id="h2"),
        )
    )
    hidden_problem = HiddenProblem("prob_b", hidden_suite=hidden_suite, judge_spec=JudgeSpec())

    executor = TrustedFixtureExecutor()
    judge_res = executor.evaluate(
        candidate=selected,
        tests=hidden_problem.hidden_suite.cases,
        spec=ExecutionSpec(),
        limits=ProblemLimits()
    )

    # Candidate A fails test 3 (got YES, expected NO)
    assert judge_res.all_passed is False
    assert judge_res.passed == 1
    assert judge_res.total == 2
    assert judge_res.pass_rate == 0.5
