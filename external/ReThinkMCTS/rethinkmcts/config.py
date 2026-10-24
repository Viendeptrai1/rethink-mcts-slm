from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SearchConfig:
    run_name: str = "rethinkmcts_v1"
    model: str | None = None
    evaluator_model: str | None = None
    rollouts: int = 16
    width: int = 3
    c_base: float = 10.0
    exploration_weight: float = 4.0
    reward_a: float = 0.8
    reward_b: float = 0.2
    reward_mode: str = "dual"
    seed: int = 0
    public_cases_type: str = "half"
    max_rethink_times: int = 2
    max_feedback_tests: int = 1
    max_trace_blocks: int = 10
    max_block_chars: int = 5000
    max_feedback_chars: int = 8000
    timeout_seconds: float = 5.0
    apps_test_workers: int = 1
    temperature: float = 0.2
    top_p: float = 0.95
    max_tokens: int | None = None
    reasoning_effort: str | None = None

    def validate(self) -> None:
        if self.reward_mode not in {"dual", "test_only"}:
            raise ValueError("reward_mode must be 'dual' or 'test_only'")
        if self.evaluator_model and self.reward_mode != "dual":
            raise ValueError("evaluator_model is only valid with reward_mode='dual'")
        if self.evaluator_model and self.model and self.evaluator_model == self.model:
            raise ValueError("evaluator_model must differ from the generation model")
        if not self.run_name.strip():
            raise ValueError("run_name must not be empty")
        if self.rollouts <= 0:
            raise ValueError("rollouts must be greater than zero")
        if self.width <= 0:
            raise ValueError("width must be greater than zero")
        if self.c_base <= 0 or self.exploration_weight < 0:
            raise ValueError("c_base must be positive and exploration weight non-negative")
        if self.reward_a < 0 or self.reward_b < 0:
            raise ValueError("reward weights must be non-negative")
        if self.reward_a + self.reward_b <= 0:
            raise ValueError("at least one reward weight must be positive")
        if self.max_rethink_times < 0:
            raise ValueError("max_rethink_times must be non-negative")
        if self.max_feedback_tests <= 0:
            raise ValueError("max_feedback_tests must be greater than zero")
        if self.max_trace_blocks <= 0 or self.max_block_chars <= 0:
            raise ValueError("trace limits must be greater than zero")
        if self.max_feedback_chars <= 0:
            raise ValueError("max_feedback_chars must be greater than zero")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        if self.apps_test_workers <= 0:
            raise ValueError("apps_test_workers must be greater than zero")
        if not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be between 0 and 2")
        if not 0 < self.top_p <= 1:
            raise ValueError("top_p must be in (0, 1]")
        if self.max_tokens is not None and self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive when set")
        if self.public_cases_type not in {"half", "half_min2"} and not self.public_cases_type.isdigit():
            raise ValueError("public_cases_type must be 'half', 'half_min2' or a positive integer")
        if self.public_cases_type.isdigit() and int(self.public_cases_type) <= 0:
            raise ValueError("public_cases_type must be positive")
