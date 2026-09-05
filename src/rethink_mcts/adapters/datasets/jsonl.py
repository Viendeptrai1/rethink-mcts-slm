"""
JSONL Dataset Source adapter implementing PublicProblemSource and HiddenSuiteSource ports.
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
    ExecutionSpec,
    ProblemLimits,
    PublicMetadata,
    JudgeSpec
)
from rethink_mcts.ports.datasets import PublicProblemSource, HiddenSuiteSource


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
                pub_tests = []
                for c in d.get("public_tests", []):
                    pub_tests.append(
                        StdinCase(
                            stdin=c["stdin"],
                            expected_stdout=c["expected_stdout"],
                            case_id=c.get("case_id", ""),
                            comparator_id=c.get("comparator_id", "token_text")
                        )
                    )
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
                    hid_cases = []
                    for c in d.get("hidden_cases", []):
                        hid_cases.append(
                            StdinCase(
                                stdin=c["stdin"],
                                expected_stdout=c["expected_stdout"],
                                case_id=c.get("case_id", ""),
                                comparator_id=c.get("comparator_id", "token_text")
                            )
                        )
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
