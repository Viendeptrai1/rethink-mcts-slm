from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CandidateRecord:
    candidate_id: str
    node_id: str
    code: str
    public_passed_tests: int
    public_total_tests: int
    public_pass_rate: float
    llm_score: float | None
    reward: float
    status: str
    feedback: dict[str, Any] | None = None
    request_ids: list[str] = field(default_factory=list)
    response_text: str | None = None
    execution: dict[str, Any] | None = None
    thoughts: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "node_id": self.node_id,
            "code": self.code,
            "public_passed_tests": self.public_passed_tests,
            "public_total_tests": self.public_total_tests,
            "public_pass_rate": self.public_pass_rate,
            "llm_score": self.llm_score,
            "reward": self.reward,
            "status": self.status,
            "feedback": self.feedback,
            "request_ids": self.request_ids,
            "response_text": self.response_text,
            "execution": self.execution,
            "thoughts": list(self.thoughts),
        }


@dataclass
class SearchNode:
    node_id: str
    thoughts: list[str] = field(default_factory=list)
    parent: "SearchNode | None" = None
    prior: float = 1.0
    action: str | None = None
    candidate_code: str | None = None
    children: list["SearchNode"] = field(default_factory=list)
    visit_count: int = 0
    q_value: float = 0.0
    feedback: dict[str, Any] | None = None
    rethink_count: int = 0
    replaced_by: str | None = None
    expansion_count: int = 0

    @property
    def is_root(self) -> bool:
        return self.parent is None

    @property
    def depth(self) -> int:
        return len(self.thoughts)

    def add_child(self, child: "SearchNode") -> None:
        if child.parent is not self:
            raise ValueError("child.parent must reference this node")
        self.children.append(child)

    def replace_last_thought(self, thought: str, *, feedback: dict[str, Any] | None = None) -> None:
        if not self.thoughts:
            raise ValueError("cannot rethink the root node")
        cleaned = thought.strip()
        if not cleaned:
            raise ValueError("replacement thought must not be empty")
        self.thoughts[-1] = cleaned
        self.action = cleaned
        self.feedback = feedback
        self.rethink_count += 1
        for child in self.children:
            child.replaced_by = self.node_id
        self.children = []
        self.expansion_count = 0
        self.visit_count = 0
        self.q_value = 0.0
        self.candidate_code = None
        self.prior = 1.0

    def path(self) -> list["SearchNode"]:
        nodes: list[SearchNode] = []
        current: SearchNode | None = self
        while current is not None:
            nodes.append(current)
            current = current.parent
        return list(reversed(nodes))

    def backpropagate(self, reward: float) -> None:
        if not 0.0 <= reward <= 1.0:
            raise ValueError("reward must be in [0, 1]")
        for node in self.path():
            node.visit_count += 1
            node.q_value = max(node.q_value, reward)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "thoughts": list(self.thoughts),
            "parent_id": self.parent.node_id if self.parent else None,
            "prior": self.prior,
            "action": self.action,
            "candidate_code": self.candidate_code,
            "visit_count": self.visit_count,
            "q_value": self.q_value,
            "feedback": self.feedback,
            "rethink_count": self.rethink_count,
            "replaced_by": self.replaced_by,
            "expansion_count": self.expansion_count,
            "children": [child.to_dict() for child in self.children],
        }
