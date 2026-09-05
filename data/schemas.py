from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TestStatus(str, Enum):
    ACCEPTED = "ACCEPTED"                     # AC
    WRONG_ANSWER = "WRONG_ANSWER"             # WA
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED" # TLE
    RUNTIME_ERROR = "RUNTIME_ERROR"           # RE
    COMPILATION_ERROR = "COMPILATION_ERROR"   # CE


class TestCase(BaseModel):
    input: str
    output: str


class Problem(BaseModel):
    id: str
    title: str
    description: str
    public_tests: List[TestCase] = Field(default_factory=list)
    private_tests: List[TestCase] = Field(default_factory=list)
    generated_tests: List[TestCase] = Field(default_factory=list)
    source: Optional[str] = None
    difficulty: Optional[str] = None
    cf_rating: Optional[int] = None
    cf_tags: List[str] = Field(default_factory=list)
    time_limit: Optional[float] = None
    solutions: List[Dict[str, Any]] = Field(default_factory=list)
    incorrect_solutions: List[Dict[str, Any]] = Field(default_factory=list)


class SingleTestResult(BaseModel):
    status: TestStatus
    input: str
    expected_output: str
    actual_output: str = ""
    error_message: str = ""
    execution_time: float = 0.0


class ExecutionResult(BaseModel):
    all_passed: bool = False
    pass_rate: float = 0.0
    passed_count: int = 0
    total_count: int = 0
    first_failed_test: Optional[SingleTestResult] = None
    test_results: List[SingleTestResult] = Field(default_factory=list)
    verbal_feedback: str = ""
