"""
APPS dataset adapter (§11.3).
Supports introductory, interview, and competition splits with call-based and stdin modes.
"""

import json
from typing import Tuple, List
from rethink_mcts.domain.problem import (
    PublicProblem,
    HiddenProblem,
    HiddenSuite,
    StdinCase,
    ExecutionSpec,
    ExecutionMode,
    ProblemLimits,
    PublicMetadata,
    JudgeSpec
)


def parse_apps_record(item: dict) -> Tuple[PublicProblem, HiddenProblem]:
    """
    Parses an APPS record:
    {
      "problem_id": 0,
      "question": "...",
      "input_output": "{\"inputs\": [...], \"outputs\": [...]}",
      "difficulty": "introductory"
    }
    """
    prob_id = f"apps_{item.get('problem_id', 0)}"
    question = item.get("question", "")
    difficulty = item.get("difficulty", "introductory")

    io_data = {}
    io_str = item.get("input_output", "")
    if io_str:
        try:
            io_data = json.loads(io_str)
        except Exception:
            pass

    inputs = io_data.get("inputs", [])
    outputs = io_data.get("outputs", [])

    all_cases: List[StdinCase] = []
    for idx, (inp, out) in enumerate(zip(inputs, outputs)):
        inp_text = "\n".join(inp) if isinstance(inp, list) else str(inp)
        out_text = "\n".join(out) if isinstance(out, list) else str(out)
        all_cases.append(
            StdinCase(
                stdin=inp_text + "\n" if not inp_text.endswith("\n") else inp_text,
                expected_stdout=out_text + "\n" if not out_text.endswith("\n") else out_text,
                case_id=f"case_{idx+1}"
            )
        )

    # First 2 cases are public examples, remainder are hidden
    pub_cases = tuple(all_cases[:2])
    hid_cases = tuple(all_cases[2:]) if len(all_cases) > 2 else tuple(all_cases)

    public_problem = PublicProblem(
        problem_id=prob_id,
        statement=question,
        execution_spec=ExecutionSpec(mode=ExecutionMode.STDIN),
        public_tests=pub_cases,
        limits=ProblemLimits(timeout_seconds=4.0),
        metadata=PublicMetadata(source="APPS", difficulty=difficulty)
    )

    hidden_problem = HiddenProblem(
        problem_id=prob_id,
        hidden_suite=HiddenSuite(cases=hid_cases, suite_id=f"{prob_id}_hidden"),
        judge_spec=JudgeSpec(timeout_seconds=4.0)
    )

    return public_problem, hidden_problem
