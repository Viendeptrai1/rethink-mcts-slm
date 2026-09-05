"""
Budget tracking and reservation domain models.
"""

import time
from dataclasses import dataclass, field
from rethink_mcts.domain.errors import BudgetExceededError


@dataclass(frozen=True)
class BudgetLimits:
    max_code_generations: int = 8
    max_search_iterations: int = 64
    max_model_calls: int = 64
    max_total_tokens: int = 65536
    max_wall_seconds: float = 900.0
    max_sandbox_runs: int = 1000


@dataclass
class Usage:
    model_calls_by_role: dict[str, int] = field(default_factory=lambda: {
        "expansion": 0,
        "code": 0,
        "rethink": 0,
        "critic": 0,
        "block_analysis": 0
    })
    transport_attempts: int = 0
    code_generation_attempts: int = 0
    valid_candidates: int = 0
    evaluation_events: int = 0
    unique_programs: int = 0
    rethink_attempts: int = 0
    sandbox_runs: int = 0
    trace_runs: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_hits: int = 0
    wall_time_seconds: float = 0.0

    @property
    def total_model_calls(self) -> int:
        return sum(self.model_calls_by_role.values())

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def to_dict(self) -> dict:
        return {
            "total_model_calls": self.total_model_calls,
            "model_calls_by_role": dict(self.model_calls_by_role),
            "transport_attempts": self.transport_attempts,
            "code_generation_attempts": self.code_generation_attempts,
            "valid_candidates": self.valid_candidates,
            "evaluation_events": self.evaluation_events,
            "unique_programs": self.unique_programs,
            "rethink_attempts": self.rethink_attempts,
            "sandbox_runs": self.sandbox_runs,
            "trace_runs": self.trace_runs,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cache_hits": self.cache_hits,
            "wall_time_seconds": round(self.wall_time_seconds, 2)
        }


class BudgetManager:
    def __init__(self, limits: BudgetLimits):
        self.limits = limits
        self.usage = Usage()
        self.start_time = time.time()

    def update_wall_time(self) -> float:
        self.usage.wall_time_seconds = time.time() - self.start_time
        return self.usage.wall_time_seconds

    def is_exhausted(self) -> tuple[bool, str]:
        elapsed = self.update_wall_time()
        if elapsed >= self.limits.max_wall_seconds:
            return True, f"Wall time limit reached ({elapsed:.1f}s >= {self.limits.max_wall_seconds}s)"
        if self.usage.code_generation_attempts >= self.limits.max_code_generations:
            return True, f"Code generation attempts limit reached ({self.usage.code_generation_attempts} >= {self.limits.max_code_generations})"
        if self.usage.total_model_calls >= self.limits.max_model_calls:
            return True, f"Total model calls limit reached ({self.usage.total_model_calls} >= {self.limits.max_model_calls})"
        if self.usage.total_tokens >= self.limits.max_total_tokens:
            return True, f"Token budget exceeded ({self.usage.total_tokens} >= {self.limits.max_total_tokens})"
        if self.usage.sandbox_runs >= self.limits.max_sandbox_runs:
            return True, f"Sandbox runs exceeded ({self.usage.sandbox_runs} >= {self.limits.max_sandbox_runs})"
        return False, ""

    def can_start_code_generation(self) -> bool:
        exhausted, _ = self.is_exhausted()
        if exhausted:
            return False
        return self.usage.code_generation_attempts < self.limits.max_code_generations

    def can_reserve_refinement_and_regeneration(self) -> bool:
        """
        §12.3: Before rethink, must have at least 1 remaining code generation slot
        and remaining call budget for both refinement and regeneration.
        """
        exhausted, _ = self.is_exhausted()
        if exhausted:
            return False
        # Needs at least 1 remaining code attempt
        if self.usage.code_generation_attempts >= self.limits.max_code_generations:
            return False
        # Needs at least 2 remaining model calls (refine + generate)
        if self.usage.total_model_calls + 2 > self.limits.max_model_calls:
            return False
        return True

    def record_model_call(
        self,
        role: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        transport_attempts: int = 1
    ) -> None:
        if role in self.usage.model_calls_by_role:
            self.usage.model_calls_by_role[role] += 1
        else:
            self.usage.model_calls_by_role[role] = 1

        self.usage.transport_attempts += transport_attempts
        self.usage.input_tokens += input_tokens
        self.usage.output_tokens += output_tokens
        self.update_wall_time()

    def record_code_generation_attempt(self) -> None:
        self.usage.code_generation_attempts += 1

    def record_rethink_attempt(self) -> None:
        self.usage.rethink_attempts += 1

    def record_evaluation_event(self) -> None:
        self.usage.evaluation_events += 1

    def record_sandbox_run(self, count: int = 1) -> None:
        self.usage.sandbox_runs += count

    def record_trace_run(self) -> None:
        self.usage.trace_runs += 1

    def record_cache_hit(self) -> None:
        self.usage.cache_hits += 1
