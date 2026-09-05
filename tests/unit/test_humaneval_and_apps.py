"""
Tests for HumanEval and APPS dataset adapters and evaluation harnesses.
"""

from rethink_mcts.adapters.datasets.humaneval import parse_humaneval_record
from rethink_mcts.adapters.datasets.apps import parse_apps_record
from rethink_mcts.adapters.execution.trusted_fixture_executor import TrustedFixtureExecutor
from rethink_mcts.domain.candidate import ProgramCandidate
from rethink_mcts.application.judge import HiddenJudge


def test_humaneval_parsing_and_execution():
    item = {
        "task_id": "HumanEval/0",
        "prompt": 'from typing import List\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    """ Check if numbers are close.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    """\n',
        "entry_point": "has_close_elements",
        "canonical_solution": "    for idx, elem in enumerate(numbers):\n        for idx2, elem2 in enumerate(numbers):\n            if idx != idx2:\n                distance = abs(elem - elem2)\n                if distance < threshold:\n                    return True\n    return False\n",
        "test": "def check(has_close_elements):\n    assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True\n    assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False\n"
    }

    public_prob, hidden_prob = parse_humaneval_record(item)

    assert public_prob.problem_id == "humaneval_0"
    assert len(public_prob.public_tests) == 2
    assert "assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False" in public_prob.public_tests[0].test_code

    # Execute canonical solution
    full_code = public_prob.statement + item["canonical_solution"]
    candidate = ProgramCandidate(
        candidate_id="cand_canonical",
        problem_id=public_prob.problem_id,
        code=full_code,
        code_hash=ProgramCandidate.compute_hash(full_code)
    )

    executor = TrustedFixtureExecutor()
    summary = executor.evaluate(
        candidate=candidate,
        tests=public_prob.public_tests,
        spec=public_prob.execution_spec,
        limits=public_prob.limits
    )
    assert summary.all_passed is True
    assert summary.passed == 2

    # Run Hidden Judge
    judge = HiddenJudge(executor=executor)
    judge_res = judge.judge(candidate, hidden_prob)
    assert judge_res.all_hidden_passed is True
    assert judge_res.hidden_passed == 1


def test_apps_parsing_and_execution():
    item = {
        "id": 101,
        "question": "Read an integer and print its square.",
        "input_output": '{"inputs": ["3\\n", "4\\n", "5\\n"], "outputs": ["9\\n", "16\\n", "25\\n"]}',
        "difficulty": "introductory"
    }

    pub_prob, hid_prob = parse_apps_record(item)
    assert pub_prob.problem_id == "apps_101"
    assert len(pub_prob.public_tests) == 2
    assert len(hid_prob.hidden_suite.cases) == 1

    solution_code = "import sys\nx = int(sys.stdin.read().strip())\nprint(x * x)"
    candidate = ProgramCandidate(
        candidate_id="cand_apps_sol",
        problem_id=pub_prob.problem_id,
        code=solution_code,
        code_hash=ProgramCandidate.compute_hash(solution_code)
    )

    executor = TrustedFixtureExecutor()
    summary = executor.evaluate(
        candidate=candidate,
        tests=pub_prob.public_tests,
        spec=pub_prob.execution_spec,
        limits=pub_prob.limits
    )
    assert summary.all_passed is True

    judge = HiddenJudge(executor=executor)
    judge_res = judge.judge(candidate, hid_prob)
    assert judge_res.all_hidden_passed is True
