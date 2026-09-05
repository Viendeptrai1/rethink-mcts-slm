"""
JSONL Dataset Source adapter implementing PublicProblemSource and HiddenSuiteSource ports.
Supports StdinCase, FunctionCase, and AssertionSuite cases polymorphically.
"""

import json
from typing import Dict, List, Optional
from rethink_mcts.domain.problem import (
    PublicProblem,
    HiddenProblem,
    HiddenSuite,
    TestCase,
    StdinCase,
    FunctionCase,
    AssertionSuite,
    ExecutionSpec,
    ProblemLimits,
    PublicMetadata,
    JudgeSpec
)
from rethink_mcts.ports.datasets import PublicProblemSource, HiddenSuiteSource


def parse_case_dict(c: dict) -> TestCase:
    if "stdin" in c:
        return StdinCase(
            stdin=c["stdin"],
            expected_stdout=c.get("expected_stdout", ""),
            case_id=c.get("case_id", ""),
            comparator_id=c.get("comparator_id", "token_text")
        )
    elif "test_code" in c:
        return AssertionSuite(
            test_code=c["test_code"],
            entry_point=c.get("entry_point", ""),
            case_id=c.get("case_id", "")
        )
    elif "entry_point" in c:
        args = c.get("args", ())
        kwargs = c.get("kwargs", {})
        return FunctionCase(
            entry_point=c["entry_point"],
            args=tuple(args) if isinstance(args, (list, tuple)) else (args,),
            kwargs=tuple(kwargs.items()) if isinstance(kwargs, dict) else tuple(kwargs),
            expected=c.get("expected"),
            case_id=c.get("case_id", "")
        )
    raise ValueError(f"Unknown test case format: {c}")


class JSONLProblemSource(PublicProblemSource, HiddenSuiteSource):
    def __init__(self, public_jsonl_path: str, hidden_jsonl_path: Optional[str] = None):
        self.public_jsonl_path = public_jsonl_path
        self.hidden_jsonl_path = hidden_jsonl_path
        self._public_problems: Dict[str, PublicProblem] = {}
        self._hidden_problems: Dict[str, HiddenProblem] = {}
        self._load_all()

    def _load_all(self):
        # Load public problems
        with open(self.public_jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                d = json.loads(line.strip())
                pub_tests = [parse_case_dict(c) for c in d.get("public_tests", [])]
                prob = PublicProblem(
                    problem_id=d["problem_id"],
                    statement=d["statement"],
                    execution_spec=ExecutionSpec(**d.get("execution_spec", {})),
                    public_tests=tuple(pub_tests),
                    limits=ProblemLimits(**d.get("limits", {})),
                    metadata=PublicMetadata(**d.get("metadata", {}))
                )
                self._public_problems[prob.problem_id] = prob

        # Load hidden problems if provided
        if self.hidden_jsonl_path:
            with open(self.hidden_jsonl_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    d = json.loads(line.strip())
                    hid_cases = [parse_case_dict(c) for c in d.get("hidden_cases", [])]
                    hid = HiddenProblem(
                        problem_id=d["problem_id"],
                        hidden_suite=HiddenSuite(cases=tuple(hid_cases)),
                        judge_spec=JudgeSpec(**d.get("judge_spec", {}))
                    )
                    self._hidden_problems[hid.problem_id] = hid

    def get_problem(self, problem_id: str) -> PublicProblem:
        return self._public_problems[problem_id]

    def list_problem_ids(self) -> tuple[str, ...]:
        return tuple(self._public_problems.keys())

    def get_hidden_problem(self, problem_id: str) -> HiddenProblem:
        return self._hidden_problems[problem_id]
