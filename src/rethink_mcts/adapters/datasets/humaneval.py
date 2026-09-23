"""
HumanEval dataset adapter matching upstream paper (§11.4).
Exposes function signature and docstrings/doctests to PublicProblem;
holds official evaluation assertion harness strictly in HiddenProblem.
"""

import doctest
from rethink_mcts.domain.errors import ConfigurationError
from typing import Tuple, List
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


def extract_doctests_from_prompt(prompt: str, entry_point: str) -> List[AssertionSuite]:
    """
    Extracts public doctest examples (>>> call) from docstrings without leaking official tests.
    """
    parser = doctest.DocTestParser()
    cases: List[AssertionSuite] = []
    try:
        examples = parser.get_examples(prompt)
        for idx, ex in enumerate(examples):
            src = ex.source.strip()
            want = ex.want.split('"""')[0].split("'''")[0].strip()
            if src and want:
                test_code = f"assert {src} == {want}"
                cases.append(
                    AssertionSuite(
                        test_code=test_code,
                        entry_point=entry_point,
                        case_id=f"doctest_{idx+1}"
                    )
                )
    except Exception:
        pass
    return cases


def parse_humaneval_record(item: dict) -> Tuple[PublicProblem, HiddenProblem]:
    """
    Parses HumanEval record (from either OpenAI HumanEval or RethinkMCTS processed.jsonl):
    {
      "task_id": "HumanEval/0" or "Python/0",
      "prompt": "...",
      "entry_point": "has_close_elements",
      "canonical_solution": "...",
      "test": "def check(candidate): ...",
      "given_tests": ["assert has_close_elements(...) == False", ...] (optional)
    }
    """
    task_id = item.get("task_id", "HumanEval/0")
    clean_id = task_id.replace("/", "_").lower()
    prompt = item.get("prompt", "")
    entry_point = item.get("entry_point", "")
    test_harness = item.get("test", "")

    # 1. Parse Public Tests
    pub_cases: List[AssertionSuite] = []
    if "given_tests" in item and item["given_tests"]:
        for idx, stmt in enumerate(item["given_tests"]):
            pub_cases.append(
                AssertionSuite(
                    test_code=str(stmt).strip(),
                    entry_point=entry_point,
                    case_id=f"given_{idx+1}"
                )
            )
    else:
        pub_cases = extract_doctests_from_prompt(prompt, entry_point)

    if not pub_cases:
        raise ConfigurationError(f"{clean_id}: no behavioral public tests; provide examples or exclude explicitly")

    public_problem = PublicProblem(
        problem_id=clean_id,
        statement=prompt,
        execution_spec=ExecutionSpec(
            mode=ExecutionMode.ASSERTION_SUITE,
            entry_point=entry_point
        ),
        public_tests=tuple(pub_cases),
        limits=ProblemLimits(timeout_seconds=3.0),
        metadata=PublicMetadata(source="HumanEval")
    )

    # 2. Hidden Problem with official check harness
    hidden_suite = HiddenSuite(
        cases=(
            AssertionSuite(
                test_code=test_harness + f"\ncheck({entry_point})",
                entry_point=entry_point,
                case_id="official_check"
            ),
        ),
        suite_id=f"{clean_id}_harness"
    )

    hidden_problem = HiddenProblem(
        problem_id=clean_id,
        hidden_suite=hidden_suite,
        judge_spec=JudgeSpec(timeout_seconds=3.0, comparator_id="benchmark_harness")
    )

    return public_problem, hidden_problem
