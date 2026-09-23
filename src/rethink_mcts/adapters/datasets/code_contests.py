"""
CodeContests dataset adapter (§11.2).
Handles deepmind/code_contests schema with strict validation and public/hidden separation.
"""

from typing import Dict, List, Optional, Tuple
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
from rethink_mcts.domain.errors import ConfigurationError


def _to_str(val) -> str:
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace")
    return str(val) if val is not None else ""


def parse_code_contests_record(
    item: dict
) -> Tuple[PublicProblem, HiddenProblem]:
    """
    Parses a single CodeContests entry into strictly separated PublicProblem and HiddenProblem.
    Validates array lengths without silent dropping (§11.2).
    """
    prob_id = str(item.get("name", "unknown_id"))
    desc = _to_str(item.get("description", ""))

    # 1. Parse Public Tests
    pub_cases: List[StdinCase] = []
    pub_dict = item.get("public_tests", {}) or {}
    pub_inputs = pub_dict.get("input", [])
    pub_outputs = pub_dict.get("output", [])
    if len(pub_inputs) != len(pub_outputs):
        raise ConfigurationError(f"Mismatched public test lengths for {prob_id}: {len(pub_inputs)} inputs vs {len(pub_outputs)} outputs")

    for i, (inp, out) in enumerate(zip(pub_inputs, pub_outputs)):
        pub_cases.append(
            StdinCase(
                stdin=_to_str(inp),
                expected_stdout=_to_str(out),
                case_id=f"pub_{i+1}",
                comparator_id="token_text"
            )
        )

    # 2. Parse Hidden / Private Tests
    priv_cases: List[StdinCase] = []
    priv_dict = item.get("private_tests", {}) or {}
    priv_inputs = priv_dict.get("input", [])
    priv_outputs = priv_dict.get("output", [])
    if len(priv_inputs) != len(priv_outputs):
        raise ConfigurationError(f"Mismatched private test lengths for {prob_id}")

    for i, (inp, out) in enumerate(zip(priv_inputs, priv_outputs)):
        priv_cases.append(
            StdinCase(
                stdin=_to_str(inp),
                expected_stdout=_to_str(out),
                case_id=f"priv_{i+1}",
                comparator_id="token_text"
            )
        )

    # Generated tests
    gen_cases: List[StdinCase] = []
    gen_dict = item.get("generated_tests", {}) or {}
    gen_inputs = gen_dict.get("input", [])
    gen_outputs = gen_dict.get("output", [])
    if len(gen_inputs) != len(gen_outputs):
        raise ConfigurationError(f"Mismatched generated test lengths for {prob_id}")
    for i, (inp, out) in enumerate(zip(gen_inputs, gen_outputs)):
        gen_cases.append(
            StdinCase(
                stdin=_to_str(inp),
                expected_stdout=_to_str(out),
                case_id=f"gen_{i+1}",
                comparator_id="token_text"
            )
        )

    cf_rating = item.get("cf_rating")
    if cf_rating is not None:
        try:
            cf_rating = int(cf_rating)
            if cf_rating <= 0:
                cf_rating = None
        except ValueError:
            cf_rating = None

    time_limit = item.get("time_limit")
    limit_sec = 2.0
    if isinstance(time_limit, dict):
        limit_sec = float(time_limit.get("seconds", 2.0))
    elif isinstance(time_limit, (int, float)):
        limit_sec = float(time_limit)

    public_problem = PublicProblem(
        problem_id=prob_id,
        statement=desc,
        execution_spec=ExecutionSpec(),
        public_tests=tuple(pub_cases),
        limits=ProblemLimits(timeout_seconds=max(2.0, limit_sec * 2.5)),
        metadata=PublicMetadata(
            source=str(item.get("source", "")),
            difficulty=str(item.get("difficulty", "")),
            cf_rating=cf_rating
        )
    )

    hidden_problem = HiddenProblem(
        problem_id=prob_id,
        hidden_suite=HiddenSuite(
            cases=tuple(priv_cases),
            suite_id=f"{prob_id}_hidden",
            generated_cases=tuple(gen_cases)
        ),
        judge_spec=JudgeSpec(timeout_seconds=limit_sec)
    )

    return public_problem, hidden_problem


def has_python3_solution(item: dict) -> bool:
    """Checks if entry has at least 1 Python 3 solution."""
    sols = item.get("solutions", {})
    if isinstance(sols, dict):
        langs = sols.get("language", [])
        return 3 in langs or "PYTHON3" in langs or "PYTHON_3" in langs
    return False
