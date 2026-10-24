from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, ConfigDict, Field, InstanceOf

from .policies import select_child
from .tree import CandidateRecord, SearchNode

if TYPE_CHECKING:
    from .search import SearchEngine


class WorkflowState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    root: InstanceOf[SearchNode]
    rollout: int = Field(default=0, ge=0)
    node: InstanceOf[SearchNode] | None = None
    candidate: InstanceOf[CandidateRecord] | None = None
    phase: Literal["initial", "rethink"] = "initial"
    retry_ready: bool = False
    best_candidate: InstanceOf[CandidateRecord] | None = None
    private_evaluation: dict | None = None


def _node(state: WorkflowState) -> SearchNode:
    if state.node is None:
        raise ValueError("workflow has no selected node")
    return state.node


def _candidate(state: WorkflowState) -> CandidateRecord:
    if state.candidate is None:
        raise ValueError("workflow has no evaluated candidate")
    return state.candidate


def build_search_graph(engine: SearchEngine):
    def choose_child(parent: SearchNode) -> SearchNode:
        return select_child(
            parent,
            c_base=engine.config.c_base,
            exploration_weight=engine.config.exploration_weight,
            rng=engine.rng,
        )

    def select(state: WorkflowState) -> dict:
        node = state.root
        while node.children:
            node = choose_child(node)
        return {"node": node, "candidate": None, "phase": "initial", "retry_ready": False}

    def expand(state: WorkflowState) -> dict:
        leaf = _node(state)
        engine._expand(leaf)
        node = choose_child(leaf)
        engine._event("select", rollout=state.rollout, node_id=node.node_id)
        return {"node": node}

    def evaluate(state: WorkflowState) -> dict:
        candidate = engine._evaluate(_node(state), phase=state.phase)
        return {"candidate": candidate}

    def route_evaluation(state: WorkflowState) -> Literal["rethink", "advance"]:
        if (
            _candidate(state).public_pass_rate < 1.0
            and _node(state).rethink_count < engine.config.max_rethink_times
        ):
            return "rethink"
        return "advance"

    def rethink(state: WorkflowState) -> dict:
        ready = engine._rethink(_node(state), _candidate(state))
        return {"retry_ready": ready, "phase": "rethink"}

    def route_rethink(state: WorkflowState) -> Literal["evaluate", "advance"]:
        return "evaluate" if state.retry_ready else "advance"

    def advance(state: WorkflowState) -> dict:
        if _candidate(state).public_pass_rate < 1.0 and state.rollout + 1 < engine.config.rollouts:
            node = _node(state)
            engine._event("rethink_next", rollout=state.rollout, node_id=node.node_id)
            engine._expand(node)
        return {"rollout": state.rollout + 1}

    def route_advance(state: WorkflowState) -> Literal["select", "finalize"]:
        return "select" if state.rollout < engine.config.rollouts else "finalize"

    def finalize(state: WorkflowState) -> dict:
        best = max(engine.candidates, key=lambda item: item.reward, default=None)
        final_evaluator = getattr(engine.executor, "evaluate_final", engine.executor.evaluate_private)
        private_evaluation = (
            final_evaluator(engine.context, best.code).to_dict()
            if best is not None
            else None
        )
        engine._event(
            "complete",
            candidate_count=len(engine.candidates),
            best_candidate_id=best.candidate_id if best else None,
            best_reward=best.reward if best else None,
        )
        return {"best_candidate": best, "private_evaluation": private_evaluation}

    graph = StateGraph(WorkflowState)
    graph.add_node("select", select)
    graph.add_node("expand", expand)
    graph.add_node("evaluate", evaluate)
    graph.add_node("rethink", rethink)
    graph.add_node("advance", advance)
    graph.add_node("finalize", finalize)
    graph.add_edge(START, "select")
    graph.add_edge("select", "expand")
    graph.add_edge("expand", "evaluate")
    graph.add_conditional_edges("evaluate", route_evaluation)
    graph.add_conditional_edges("rethink", route_rethink)
    graph.add_conditional_edges("advance", route_advance)
    graph.add_edge("finalize", END)
    return graph.compile()
