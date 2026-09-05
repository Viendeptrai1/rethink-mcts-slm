"""
Output comparators matching §10.3 of RethinkMCTS spec.
"""

import math
from typing import Any


def compare_token_text(actual: str, expected: str) -> bool:
    """
    Compares outputs by tokenized whitespace equality.
    Handles trailing newlines and whitespace differences cleanly.
    """
    act_tokens = actual.strip().split()
    exp_tokens = expected.strip().split()
    return act_tokens == exp_tokens


def compare_exact_text(actual: str, expected: str) -> bool:
    """
    Compares outputs with normalized newlines and trimmed trailing line whitespace.
    """
    act_lines = [line.rstrip() for line in actual.strip().splitlines()]
    exp_lines = [line.rstrip() for line in expected.strip().splitlines()]
    return "\n".join(act_lines) == "\n".join(exp_lines)


def compare_numeric(actual: str, expected: str, tol: float = 1e-6) -> bool:
    """
    Compares numeric float tokens with absolute/relative tolerance.
    """
    try:
        act_val = float(actual.strip())
        exp_val = float(expected.strip())
        if math.isnan(act_val) or math.isnan(exp_val):
            return False
        return abs(act_val - exp_val) <= tol or abs(act_val - exp_val) / max(abs(exp_val), 1e-9) <= tol
    except ValueError:
        return False


def compare_structured(actual: Any, expected: Any) -> bool:
    """
    Compares structured return values (lists, dicts, primitives).
    """
    return actual == expected


def get_comparator(comparator_id: str):
    if comparator_id == "token_text":
        return compare_token_text
    elif comparator_id == "exact_text":
        return compare_exact_text
    elif comparator_id == "numeric":
        return compare_numeric
    elif comparator_id == "structured":
        return compare_structured
    return compare_token_text
