"""Public-only, deterministic feedback selection. No hidden outcomes are inputs."""
from dataclasses import dataclass


@dataclass(frozen=True)
class FeedbackObservation:
    failure_kind: str
    pass_rate: float
    code_hash: str


@dataclass(frozen=True)
class FeedbackDecision:
    level: str
    reason: str
    stagnation: int


def select_feedback(mode, current, previous=(), escalate_after=1):
    if mode != "adaptive":
        return FeedbackDecision(mode, "fixed_policy", 0)
    stagnant = 0
    cursor = current
    for old in reversed(previous):
        if cursor.pass_rate > old.pass_rate and cursor.code_hash != old.code_hash:
            break
        stagnant += 1
        cursor = old
    # Syntax errors have no executable trace; timeout tracing adds no safe signal.
    if current.failure_kind in ("CE", "TLE"):
        return FeedbackDecision("facts_only", "non_traceable_failure", stagnant)
    base = 1 if current.failure_kind == "WA" else 0
    rank = min(2, base + stagnant // escalate_after)
    return FeedbackDecision(("facts_only", "trace", "block")[rank],
                            "public_failure_and_stagnation", stagnant)
