"""
Problem domain contracts and test visibility separation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Union


class ExecutionMode(str, Enum):
    STDIN = "stdin"
    FUNCTION = "function"
    CLASS_METHOD = "class_method"
    ASSERTION_SUITE = "assertion_suite"


@dataclass(frozen=True)
class StdinCase:
    stdin: str
    expected_stdout: str
    case_id: str = ""
    comparator_id: str = "token_text"


@dataclass(frozen=True)
class FunctionCase:
    entry_point: str
    args: tuple[Any, ...] = field(default_factory=tuple)
    kwargs: tuple[tuple[str, Any], ...] = field(default_factory=tuple)
    expected: Any = None
    case_id: str = ""
    comparator_id: str = "structured"


@dataclass(frozen=True)
class AssertionSuite:
    test_code: str
    entry_point: Optional[str] = None
    case_id: str = ""
    comparator_id: str = "benchmark_harness"


TestCase = Union[StdinCase, FunctionCase, AssertionSuite]


@dataclass(frozen=True)
class ExecutionSpec:
    mode: ExecutionMode = ExecutionMode.STDIN
    entry_point: Optional[str] = None
    signature: Optional[str] = None
    starter_code: Optional[str] = None


@dataclass(frozen=True)
class ProblemLimits:
    timeout_seconds: float = 2.0
    memory_mb: int = 512
    stdout_limit_bytes: int = 1048576  # 1 MiB


@dataclass(frozen=True)
class PublicMetadata:
    source: str = ""
    split: str = ""
    difficulty: Optional[str] = None
    cf_rating: Optional[int] = None
    runtime_notes: str = ""


@dataclass(frozen=True)
class PublicProblem:
    """
    Public problem contract visible to MCTS search, prompt generation and public evaluation.
    MUST NOT contain private/hidden tests or reference solutions.
    """
    problem_id: str
    statement: str
    execution_spec: ExecutionSpec
    public_tests: tuple[TestCase, ...]
    limits: ProblemLimits = field(default_factory=ProblemLimits)
    metadata: PublicMetadata = field(default_factory=PublicMetadata)

    def __post_init__(self):
        if not self.problem_id:
            raise ValueError("problem_id cannot be empty")
        if not self.statement:
            raise ValueError("statement cannot be empty")


@dataclass(frozen=True)
class HiddenSuite:
    cases: tuple[TestCase, ...]
    suite_id: str = "hidden_default"
    generated_cases: tuple[TestCase, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class JudgeSpec:
    timeout_seconds: float = 2.0
    memory_mb: int = 512
    comparator_id: str = "token_text"


@dataclass(frozen=True)
class HiddenProblem:
    """
    Hidden test suite held strictly outside the search loop, evaluated only by Judge.
    """
    problem_id: str
    hidden_suite: HiddenSuite
    judge_spec: JudgeSpec = field(default_factory=JudgeSpec)
