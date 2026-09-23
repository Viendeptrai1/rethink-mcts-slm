"""
APPS dataset adapter matching paper (§11.3).
Supports introductory, interview, and competition splits with call-based and stdin modes.
"""

import json
from rethink_mcts.domain.errors import ConfigurationError
from typing import Tuple, List, Union
from dataclasses import asdict
from rethink_mcts.domain.problem import (
    PublicProblem,
    HiddenProblem,
    HiddenSuite,
    StdinCase,
    FunctionCase,
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
      "id": 0 (or "problem_id": 0),
      "question": "...",
      "input_output": "{\"inputs\": [...], \"outputs\": [...], \"fn_name\": ...}",
      "difficulty": "introductory" | "interview" | "competition"
    }
    """
    raw_id = item.get("id", item.get("problem_id", 0))
    prob_id = f"apps_{raw_id}"
    question = item.get("question", "")
    difficulty = item.get("difficulty", "introductory")

    io_data = {}
    io_str = item.get("input_output", "")
    if isinstance(io_str, str) and io_str.strip():
        try:
            io_data = json.loads(io_str)
        except Exception:
            io_data = {}
    elif isinstance(io_str, dict):
        io_data = io_str

    fn_name = io_data.get("fn_name")
    inputs = io_data.get("inputs", [])
    outputs = io_data.get("outputs", [])

    if len(inputs) != len(outputs):
        raise ConfigurationError(f"{prob_id}: input/output counts differ")
    if len(inputs) < 3:
        raise ConfigurationError(f"{prob_id}: need at least 3 tests for disjoint public/hidden split")

    all_cases: List[Union[StdinCase, FunctionCase]] = []

    if fn_name:
        # Call-based / Function mode
        mode = ExecutionMode.FUNCTION
        for idx, (inp, out) in enumerate(zip(inputs, outputs)):
            args = tuple(inp) if isinstance(inp, list) else (inp,)
            all_cases.append(
                FunctionCase(
                    entry_point=fn_name,
                    args=args,
                    expected=out,
                    case_id=f"case_{idx+1}"
                )
            )
    else:
        # Standard input / output mode
        mode = ExecutionMode.STDIN
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

    # First 2 cases are public examples for MCTS search; remainder are hidden tests for judge
    pub_cases = tuple(all_cases[:2])
    def case_key(case):
        return json.dumps({k: v for k, v in asdict(case).items() if k != "case_id"}, sort_keys=True)
    public_keys = {case_key(c) for c in pub_cases}
    hid_cases = tuple(c for c in all_cases[2:] if case_key(c) not in public_keys)
    if not hid_cases:
        raise ConfigurationError(f"{prob_id}: no hidden cases remain after removing public duplicates")

    public_problem = PublicProblem(
        problem_id=prob_id,
        statement=question,
        execution_spec=ExecutionSpec(mode=mode, entry_point=fn_name),
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
