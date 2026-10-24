from __future__ import annotations


def compute_reward(
    public_pass_rate: float,
    llm_score: float | None = None,
    *,
    a: float = 0.8,
    b: float = 0.2,
) -> float:
    if not 0.0 <= public_pass_rate <= 1.0:
        raise ValueError("public_pass_rate must be in [0, 1]")
    if a < 0 or b < 0 or a + b <= 0:
        raise ValueError("reward weights must be non-negative and not both zero")
    if public_pass_rate < 1.0:
        return public_pass_rate
    if llm_score is None:
        raise ValueError("llm_score is required when public_pass_rate is 1")
    if not -1.0 <= llm_score <= 1.0:
        raise ValueError("llm_score must be in [-1, 1]")
    return max(0.0, min(1.0, a * public_pass_rate + b * llm_score))
