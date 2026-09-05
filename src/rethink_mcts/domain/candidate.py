"""
Candidate program and evaluation domain contracts.
"""

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class CandidateVerdict(str, Enum):
    AC = "AC"                    # Accepted
    WA = "WA"                    # Wrong Answer
    CE = "CE"                    # Compilation / Syntax Error
    RE = "RE"                    # Runtime Error
    TLE = "TLE"                  # Time Limit Exceeded
    MLE = "MLE"                  # Memory Limit Exceeded
    OLE = "OLE"                  # Output Limit Exceeded
    INFRA_ERROR = "INFRA_ERROR"  # Infrastructure / Container / Worker failure
    CANCELLED = "CANCELLED"      # User / Budget cancellation
    NO_TESTS = "NO_TESTS"        # Suite is empty
    INCOMPLETE = "INCOMPLETE"    # Partial execution due to budget cutoff


@dataclass(frozen=True)
class SingleCaseResult:
    case_id: str
    status: CandidateVerdict
    actual_output: Optional[str] = None
    expected_output: Optional[str] = None
    error_message: Optional[str] = None
    execution_time: float = 0.0


@dataclass(frozen=True)
class ExecutionSummary:
    total: int
    executed: int
    passed: int
    failed: int
    pass_rate: Optional[float]
    all_passed: bool
    case_results: tuple[SingleCaseResult, ...] = field(default_factory=tuple)
    first_failed_case: Optional[SingleCaseResult] = None
    elapsed_seconds: float = 0.0

    @classmethod
    def empty(cls) -> "ExecutionSummary":
        return cls(
            total=0,
            executed=0,
            passed=0,
            failed=0,
            pass_rate=None,
            all_passed=False,
            case_results=()
        )

    @classmethod
    def create(
        cls,
        total: int,
        case_results: tuple[SingleCaseResult, ...],
        elapsed_seconds: float = 0.0
    ) -> "ExecutionSummary":
        if total == 0:
            return cls(
                total=0,
                executed=0,
                passed=0,
                failed=0,
                pass_rate=None,
                all_passed=False,
                case_results=(),
                elapsed_seconds=elapsed_seconds
            )

        executed = len(case_results)
        passed = sum(1 for r in case_results if r.status == CandidateVerdict.AC)
        failed = executed - passed
        first_failed = next((r for r in case_results if r.status != CandidateVerdict.AC), None)

        # Invariant: all_passed only when all tests executed and passed
        all_passed = (total > 0 and executed == total and passed == total)
        pass_rate = (passed / total) if total > 0 else None

        return cls(
            total=total,
            executed=executed,
            passed=passed,
            failed=failed,
            pass_rate=pass_rate,
            all_passed=all_passed,
            case_results=case_results,
            first_failed_case=first_failed,
            elapsed_seconds=elapsed_seconds
        )


class CandidateOrigin(str, Enum):
    INITIAL = "initial"
    RETHINK = "rethink"
    BASELINE = "baseline"


@dataclass(frozen=True)
class ProgramCandidate:
    """
    Immutable candidate program produced by model generation.
    """
    candidate_id: str
    problem_id: str
    code: str
    code_hash: str
    language: str = "python"
    node_id: Optional[str] = None
    revision_id: Optional[str] = None
    thought_path_snapshot: tuple[str, ...] = field(default_factory=tuple)
    origin: CandidateOrigin = CandidateOrigin.INITIAL
    generation_record_id: Optional[str] = None
    created_sequence: int = 0

    @staticmethod
    def compute_hash(code: str) -> str:
        return hashlib.sha256(code.strip().encode("utf-8")).hexdigest()[:16]


class SelfEvalStatus(str, Enum):
    EVALUATED = "evaluated"
    SKIPPED_NOT_ALL_PASSED = "skipped_not_all_passed"
    UNAVAILABLE_FALLBACK = "unavailable_fallback"
    MALFORMED_RETRY_FAILED = "malformed_retry_failed"


@dataclass(frozen=True)
class EvaluationRecord:
    """
    Immutable record of evaluating a candidate against a test suite.
    """
    evaluation_id: str
    candidate_id: str
    suite_visibility: str = "public"  # "public" | "hidden"
    suite_hash: str = ""
    execution_summary: ExecutionSummary = field(default_factory=ExecutionSummary.empty)
    v_test: Optional[float] = None
    self_eval_raw: Optional[float] = None
    self_eval_status: SelfEvalStatus = SelfEvalStatus.SKIPPED_NOT_ALL_PASSED
    reward: Optional[float] = None
    reward_policy_id: str = "dual"
    feedback_id: Optional[str] = None
    backup_committed: bool = False
