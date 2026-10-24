from __future__ import annotations

import math
import random
from typing import Iterable

from .tree import SearchNode


def beta(parent_visits: int, *, c_base: float = 10.0, exploration_weight: float = 4.0) -> float:
    if parent_visits < 0:
        raise ValueError("parent_visits must be non-negative")
    if c_base <= 0 or exploration_weight < 0:
        raise ValueError("invalid P-UCB parameters")
    return math.log((parent_visits + c_base + 1) / c_base) + exploration_weight


def p_ucb_score(
    parent: SearchNode,
    child: SearchNode,
    *,
    c_base: float = 10.0,
    exploration_weight: float = 4.0,
) -> float:
    if child.parent is not parent:
        raise ValueError("child does not belong to parent")
    if parent.visit_count <= 1:
        exploration = 0.0
    else:
        exploration = (
            beta(
                parent.visit_count,
                c_base=c_base,
                exploration_weight=exploration_weight,
            )
            * child.prior
            * math.sqrt(math.log(parent.visit_count))
            / (1 + child.visit_count)
        )
    return child.q_value + exploration


def select_child(
    parent: SearchNode,
    children: Iterable[SearchNode] | None = None,
    *,
    c_base: float = 10.0,
    exploration_weight: float = 4.0,
    rng: random.Random | None = None,
) -> SearchNode:
    available = list(parent.children if children is None else children)
    if not available:
        raise ValueError("cannot select from an empty child list")
    scores = [
        p_ucb_score(parent, child, c_base=c_base, exploration_weight=exploration_weight)
        for child in available
    ]
    best = max(scores)
    tied = [child for child, score in zip(available, scores) if math.isclose(score, best, rel_tol=1e-12, abs_tol=1e-12)]
    return rng.choice(tied) if rng is not None else tied[0]
