"""
Tree, SearchNode, ThoughtRevision and proposal domain contracts.
"""

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class NodeStatus(str, Enum):
    UNEVALUATED = "UNEVALUATED"
    EVALUATING = "EVALUATING"
    READY = "READY"
    CLOSED = "CLOSED"


class CloseReason(str, Enum):
    NONE = "none"
    DEPTH_LIMIT = "depth_limit"
    NO_VALID_PROPOSALS = "no_valid_proposals"
    CONTEXT_LIMIT = "context_limit"
    GENERATION_FAILURES = "generation_failures"
    EXHAUSTED = "exhausted"
    BUDGET_REACHED = "budget_reached"


@dataclass(frozen=True)
class ThoughtProposal:
    text: str
    raw_reasonableness: float
    normalized_prior: float
    generation_record_id: Optional[str] = None


@dataclass(frozen=True)
class ProposalBatch:
    batch_id: str
    proposals: tuple[ThoughtProposal, ...]
    raw_response_ref: Optional[str] = None


@dataclass(frozen=True)
class ThoughtRevision:
    revision_id: str
    node_id: str
    thought_text: str
    parent_revision_path_hash: str
    replaces_revision_id: Optional[str] = None
    feedback_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)


@dataclass
class SearchNode:
    """
    Mutable state node in the search tree.
    Tracks logic position (node_id) and points to active thought revision (active_revision_id).
    """
    node_id: str
    parent_id: Optional[str] = None
    depth: int = 0
    active_revision_id: str = ""
    prior: float = 1.0
    child_ids: list[str] = field(default_factory=list)
    status: NodeStatus = NodeStatus.UNEVALUATED
    close_reason: CloseReason = CloseReason.NONE
    visits: int = 0
    q_max: float = 0.0
    latest_evaluation_id: Optional[str] = None
    active_feedback_id: Optional[str] = None
    expansion_attempts: int = 0
    rethink_count: int = 0

    def is_leaf(self) -> bool:
        return len(self.child_ids) == 0

    def mark_closed(self, reason: CloseReason) -> None:
        self.status = NodeStatus.CLOSED
        self.close_reason = reason


@dataclass
class Tree:
    root_id: str
    nodes: dict[str, SearchNode] = field(default_factory=dict)
    revisions: dict[str, ThoughtRevision] = field(default_factory=dict)

    @classmethod
    def create_root(cls, problem_id: str) -> "Tree":
        root_id = "root"
        root_revision_id = f"rev_{root_id}_0"
        root_revision = ThoughtRevision(
            revision_id=root_revision_id,
            node_id=root_id,
            thought_text="",
            parent_revision_path_hash="root",
            created_at=time.time()
        )
        root_node = SearchNode(
            node_id=root_id,
            parent_id=None,
            depth=0,
            active_revision_id=root_revision_id,
            prior=1.0,
            status=NodeStatus.READY  # Root is ready to be expanded
        )
        return cls(
            root_id=root_id,
            nodes={root_id: root_node},
            revisions={root_revision_id: root_revision}
        )

    def get_node(self, node_id: str) -> SearchNode:
        return self.nodes[node_id]

    def get_revision(self, revision_id: str) -> ThoughtRevision:
        return self.revisions[revision_id]

    def get_active_thought_path(self, node_id: str) -> tuple[str, ...]:
        """
        Extract active sequence of thoughts from root down to node_id.
        Excludes the empty root thought.
        """
        path = []
        curr_id = node_id
        while curr_id is not None:
            node = self.nodes[curr_id]
            rev = self.revisions[node.active_revision_id]
            if rev.thought_text:
                path.append(rev.thought_text)
            curr_id = node.parent_id
        return tuple(reversed(path))

    def get_active_thought_path_to_parent(self, node_id: str) -> tuple[str, ...]:
        """
        Extract active sequence of thoughts from root down to parent of node_id.
        """
        node = self.nodes[node_id]
        if node.parent_id is None:
            return ()
        return self.get_active_thought_path(node.parent_id)

    def create_child_node(
        self,
        parent_id: str,
        proposal: ThoughtProposal,
        parent_path_hash: str
    ) -> SearchNode:
        parent = self.nodes[parent_id]
        child_id = f"n_{len(self.nodes)}_{uuid.uuid4().hex[:6]}"
        rev_id = f"rev_{child_id}_0"

        revision = ThoughtRevision(
            revision_id=rev_id,
            node_id=child_id,
            thought_text=proposal.text,
            parent_revision_path_hash=parent_path_hash
        )
        self.revisions[rev_id] = revision

        child = SearchNode(
            node_id=child_id,
            parent_id=parent_id,
            depth=parent.depth + 1,
            active_revision_id=rev_id,
            prior=proposal.normalized_prior,
            status=NodeStatus.UNEVALUATED
        )
        self.nodes[child_id] = child
        parent.child_ids.append(child_id)
        return child

    def begin_leaf_revision(
        self,
        node_id: str,
        new_thought_text: str,
        feedback_id: Optional[str] = None
    ) -> ThoughtRevision:
        """
        Performs leaf revision according to §7.5 of spec:
        1. Node must have no children.
        2. Create new ThoughtRevision pointing to replaces_revision_id.
        3. Reset leaf visits=0, q_max=0.0, status=EVALUATING.
        4. Prior is preserved from pre_refinement proposal batch.
        """
        node = self.nodes[node_id]
        if not node.is_leaf():
            raise ValueError(f"Cannot revise node {node_id} because it already has children")

        old_rev_id = node.active_revision_id
        rev_count = node.rethink_count + 1
        new_rev_id = f"rev_{node_id}_{rev_count}"

        parent_path_hash = self.get_active_thought_path_to_parent(node_id)
        path_hash_str = str(hash(parent_path_hash))

        new_revision = ThoughtRevision(
            revision_id=new_rev_id,
            node_id=node_id,
            thought_text=new_thought_text,
            parent_revision_path_hash=path_hash_str,
            replaces_revision_id=old_rev_id,
            feedback_id=feedback_id,
            created_at=time.time()
        )
        self.revisions[new_rev_id] = new_revision

        # Update node statistics for active revision
        node.active_revision_id = new_rev_id
        node.rethink_count += 1
        node.visits = 0
        node.q_max = 0.0
        node.latest_evaluation_id = None
        node.status = NodeStatus.EVALUATING

        return new_revision
