"""
FileSystemRunStore implementing RunStore port matching §13.2 and §13.3 of spec.
Uses atomic file writing and durable directory layout.
"""

import os
import json
import yaml
from typing import Optional
from rethink_mcts.domain.candidate import ProgramCandidate, EvaluationRecord
from rethink_mcts.domain.events import EventEnvelope
from rethink_mcts.domain.tree import Tree
from rethink_mcts.domain.budget import Usage
from rethink_mcts.ports.storage import RunStore


class FileSystemRunStore(RunStore):
    def __init__(self, run_dir: str):
        self.run_dir = run_dir
        os.makedirs(self.run_dir, exist_ok=True)
        self.events_path = os.path.join(self.run_dir, "events.jsonl")

    def _problem_dir(self, problem_id: str) -> str:
        pdir = os.path.join(self.run_dir, "problems", problem_id)
        os.makedirs(pdir, exist_ok=True)
        os.makedirs(os.path.join(pdir, "programs"), exist_ok=True)
        return pdir

    def append_event(self, event: EventEnvelope) -> None:
        line = json.dumps({
            "schema_version": event.schema_version,
            "event_id": event.event_id,
            "sequence": event.sequence,
            "run_id": event.run_id,
            "problem_id": event.problem_id,
            "timestamp": event.timestamp,
            "event_type": event.event_type,
            "payload": event.payload
        }) + "\n"
        with open(self.events_path, "a", encoding="utf-8") as f:
            f.write(line)

    def save_candidate(self, candidate: ProgramCandidate) -> None:
        pdir = self._problem_dir(candidate.problem_id)
        # 1. Save raw source
        prog_path = os.path.join(pdir, "programs", f"{candidate.code_hash}.py")
        with open(prog_path, "w", encoding="utf-8") as f:
            f.write(candidate.code)

        # 2. Append to candidates.jsonl
        cand_meta = {
            "candidate_id": candidate.candidate_id,
            "problem_id": candidate.problem_id,
            "code_hash": candidate.code_hash,
            "node_id": candidate.node_id,
            "revision_id": candidate.revision_id,
            "thought_path_snapshot": list(candidate.thought_path_snapshot),
            "origin": candidate.origin.value,
            "created_sequence": candidate.created_sequence
        }
        with open(os.path.join(pdir, "candidates.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(cand_meta) + "\n")

    def save_evaluation(self, evaluation: EvaluationRecord) -> None:
        eval_meta = {
            "evaluation_id": evaluation.evaluation_id,
            "candidate_id": evaluation.candidate_id,
            "suite_visibility": evaluation.suite_visibility,
            "suite_hash": evaluation.suite_hash,
            "v_test": evaluation.v_test,
            "self_eval_raw": evaluation.self_eval_raw,
            "self_eval_status": evaluation.self_eval_status.value,
            "reward": evaluation.reward,
            "all_passed": evaluation.execution_summary.all_passed,
            "passed": evaluation.execution_summary.passed,
            "total": evaluation.execution_summary.total,
            "elapsed_seconds": evaluation.execution_summary.elapsed_seconds
        }
        # Save to general run evaluations
        eval_path = os.path.join(self.run_dir, "evaluations.jsonl")
        with open(eval_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(eval_meta) + "\n")

    def save_selected_candidate(self, problem_id: str, candidate: ProgramCandidate) -> None:
        pdir = self._problem_dir(problem_id)
        selected_meta = {
            "problem_id": problem_id,
            "candidate_id": candidate.candidate_id,
            "code_hash": candidate.code_hash,
            "origin": candidate.origin.value
        }
        with open(os.path.join(pdir, "selected.json"), "w", encoding="utf-8") as f:
            json.dump(selected_meta, f, indent=2)

        with open(os.path.join(pdir, "selected.py"), "w", encoding="utf-8") as f:
            f.write(candidate.code)

    def save_checkpoint(self, problem_id: str, tree: Tree, selected_candidate_id: Optional[str]) -> None:
        pdir = self._problem_dir(problem_id)
        tree_dict = {
            "root_id": tree.root_id,
            "selected_candidate_id": selected_candidate_id,
            "nodes": {
                nid: {
                    "node_id": n.node_id,
                    "parent_id": n.parent_id,
                    "depth": n.depth,
                    "active_revision_id": n.active_revision_id,
                    "prior": n.prior,
                    "child_ids": list(n.child_ids),
                    "status": n.status.value,
                    "visits": n.visits,
                    "q_max": n.q_max,
                    "rethink_count": n.rethink_count
                }
                for nid, n in tree.nodes.items()
            },
            "revisions": {
                rid: {
                    "revision_id": r.revision_id,
                    "node_id": r.node_id,
                    "thought_text": r.thought_text,
                    "replaces_revision_id": r.replaces_revision_id
                }
                for rid, r in tree.revisions.items()
            }
        }
        # Atomic write with temp file
        temp_path = os.path.join(pdir, "checkpoint.tmp")
        final_path = os.path.join(pdir, "checkpoint.json")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(tree_dict, f, indent=2)
        os.replace(temp_path, final_path)

    def save_usage(self, usage: Usage) -> None:
        with open(os.path.join(self.run_dir, "usage.json"), "w", encoding="utf-8") as f:
            json.dump(usage.to_dict(), f, indent=2)
