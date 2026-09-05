"""
Contract tests I22, I23, I24 for test leakage prevention, harnesses, and dataset validation.
"""

import pytest
from rethink_mcts.domain.problem import (
    PublicProblem,
    HiddenProblem,
    HiddenSuite,
    StdinCase,
    ExecutionSpec,
    ExecutionMode
)
from rethink_mcts.adapters.execution.harnesses import wrap_code_for_execution
from rethink_mcts.domain.problem import FunctionCase
from rethink_mcts.domain.errors import ConfigurationError
from rethink_mcts.adapters.datasets.code_contests import parse_code_contests_record


def test_i22_adversarial_hidden_sentinel_never_leaks_to_public():
    """
    I22: Hidden sentinel -> Không rò vào public process inputs/prompts/artifacts.
    """
    secret_sentinel = "SECRET_SENTINEL_XYZ_987"

    # Public problem
    public_problem = PublicProblem(
        problem_id="prob_leak_test",
        statement="Calculate sum of two numbers.",
        execution_spec=ExecutionSpec(),
        public_tests=(
            StdinCase(stdin="1 2\n", expected_stdout="3\n", case_id="pub_1"),
        )
    )

    # Hidden suite contains the secret sentinel
    hidden_suite = HiddenSuite(
        cases=(
            StdinCase(stdin=f"{secret_sentinel}\n", expected_stdout="SPECIAL_OUTPUT\n", case_id="hid_1"),
        )
    )
    hidden_problem = HiddenProblem("prob_leak_test", hidden_suite=hidden_suite)

    # Assert that PublicProblem object has no reference to hidden_problem or secret_sentinel
    assert not hasattr(public_problem, "hidden_suite")
    assert not hasattr(public_problem, "private_tests")
    assert secret_sentinel not in str(public_problem)
    assert secret_sentinel not in public_problem.statement
    assert all(secret_sentinel not in c.stdin for c in public_problem.public_tests)


def test_i23_function_mode_harness_preserves_function_call():
    """
    I23: Function mode -> Harness preserves entry point and does not force sys.stdin.
    """
    spec = ExecutionSpec(mode=ExecutionMode.FUNCTION, entry_point="add_two")
    case = FunctionCase(entry_point="add_two", args=(5, 10), kwargs=(), expected=15)
    code = "def add_two(a, b):\n    return a + b"

    wrapped = wrap_code_for_execution(code, case, spec)
    assert "add_two" in wrapped
    assert "json.loads" in wrapped
    assert "def add_two" in wrapped


def test_i24_mismatched_test_array_lengths_raises_error():
    """
    I24: Dataset schema error -> Fail rõ ràng, không silently drop tests.
    """
    invalid_item = {
        "name": "bad_item",
        "description": "desc",
        "public_tests": {
            "input": ["1\n", "2\n"],
            "output": ["1\n"]  # Only 1 output for 2 inputs!
        }
    }
    with pytest.raises(ConfigurationError):
        parse_code_contests_record(invalid_item)
