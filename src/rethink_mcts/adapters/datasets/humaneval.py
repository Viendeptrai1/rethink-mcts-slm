"""
HumanEval dataset adapter (§11.4).
Exposes function signature and docstrings to PublicProblem;
holds official evaluation assertion harness strictly in HiddenProblem.
"""

from typing import Tuple
from rethink_mcts.domain.problem import (
    PublicProblem,
    HiddenProblem,
    HiddenSuite,
    AssertionSuite,
    ExecutionSpec,
    ExecutionMode,
    ProblemLimits,
    PublicMetadata,
    JudgeSpec
)


def parse_humaneval_record(item: dict) -> Tuple[PublicProblem, HiddenProblem]:
    """
    Parses OpenAI HumanEval record:
    {
      "task_id": "HumanEval/0",
      "prompt": "...",
      "entry_point": "has_close_elements",
      "canonical_solution": "...",
      "test": "def check(candidate): ..."
    }
    """
    task_id = item["task_id"]
    prompt = item["prompt"]
    entry_point = item["entry_point"]
    test_harness = item["test"]

    # In HumanEval, public tests can be empty unless parsed from docstring examples,
    # so we create a dummy self-contained sanity test or assertion suite for public evaluation if needed
    public_problem = PublicProblem(
        problem_id=task_id,
        statement=prompt,
        execution_spec=ExecutionSpec(
            mode=ExecutionMode.FUNCTION,
            entry_point=entry_point
        ),
        public_tests=(),
        limits=ProblemLimits(timeout_seconds=3.0),
        metadata=PublicMetadata(source="HumanEval")
    )

    hidden_suite = HiddenSuite(
        cases=(
            AssertionSuite(
                test_code=test_harness + f"\ncheck({entry_point})",
                entry_point=entry_point,
                case_id="official_check"
            ),
        ),
        suite_id=f"{task_id}_harness"
    )

    hidden_problem = HiddenProblem(
        problem_id=task_id,
        hidden_suite=hidden_suite,
        judge_spec=JudgeSpec(timeout_seconds=3.0, comparator_id="benchmark_harness")
    )

    return public_problem, hidden_problem
