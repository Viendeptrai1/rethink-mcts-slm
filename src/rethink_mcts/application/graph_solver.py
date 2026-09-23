"""
Graph Engineering Solver (§ Graph-of-Thoughts / Flow Engineering).
Decomposes reasoning into an explicit Directed Acyclic Graph (DAG) with feedback:
1. Node_Analyze: Spec & Edge Case Identification
2. Node_MultiDraft: Multi-Angle Strategy Generation (Branching)
3. Node_Aggregate: GoT Merge Operator (Synthesis)
4. Node_Sandbox: Execution & Verification
5. Node_DiagnosePatch: Targeted Root-Cause Diagnosis & Self-Repair Loop
"""

import os
import re
import uuid
from typing import Optional, Tuple
from jinja2 import Environment, FileSystemLoader

from rethink_mcts.domain.problem import PublicProblem
from rethink_mcts.domain.candidate import ProgramCandidate, CandidateOrigin
from rethink_mcts.domain.tree import Tree
from rethink_mcts.domain.budget import BudgetLimits, BudgetManager
from rethink_mcts.ports.models import GenerationRequest, ModelGateway
from rethink_mcts.policies.final_selection import FinalSelectionPolicy
from rethink_mcts.application.candidate_archive import CandidateArchive
from rethink_mcts.application.evaluate import CandidateEvaluator
from rethink_mcts.application.search import SearchResult


def extract_robust_code(raw_text: str) -> str:
    """Extracts Python code safely without crashing on multiple fences."""
    text = raw_text.strip()
    blocks = re.findall(r"```(?:python)?\s*\n(.*?)\n```", text, re.DOTALL)
    if blocks:
        return max(blocks, key=len).strip()
    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()
        if len(lines) >= 2:
            return "\n".join(lines[1:-1]).strip()
    return text


def extract_draft_codeblocks(raw_text: str) -> Tuple[str, str]:
    """Extracts Strategy A and Strategy B code blocks from multi-draft response."""
    blocks = re.findall(r"```(?:python)?\s*\n(.*?)\n```", raw_text, re.DOTALL)
    if len(blocks) >= 2:
        return blocks[0].strip(), blocks[1].strip()
    elif len(blocks) == 1:
        return blocks[0].strip(), blocks[0].strip()
    return raw_text.strip(), raw_text.strip()


class GraphSolver:
    """
    Graph-of-Thoughts / Flow Engineering solver implementing BaseSolver interface.
    """
    def __init__(
        self,
        gateway: ModelGateway,
        evaluator: CandidateEvaluator,
        budget_limits: BudgetLimits,
        prompts_dir: str = "prompts/compact_v1",
        max_patches: int = 2
    ):
        self.gateway = gateway
        self.evaluator = evaluator
        self.budget_limits = budget_limits
        self.prompts_dir = prompts_dir
        self.max_patches = max_patches

        if not os.path.exists(prompts_dir):
            base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            self.prompts_dir = os.path.join(base, prompts_dir)

        self.env = Environment(loader=FileSystemLoader(self.prompts_dir))

    def _call_llm(self, prompt: str, role: str, temperature: float = 0.2, max_tokens: int = 1536) -> str:
        req = GenerationRequest(
            request_id=f"req_graph_{uuid.uuid4().hex[:8]}",
            role=role,
            prompt=prompt,
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        resp = self.gateway.complete(req)
        return resp.content

    def _format_public_examples(self, problem: PublicProblem) -> str:
        if not problem.public_tests:
            return ""
        ex_lines = []
        for idx, tc in enumerate(problem.public_tests[:3], start=1):
            if hasattr(tc, "assertion") and tc.assertion:
                ex_lines.append(f"Example {idx}: {tc.assertion}")
            elif hasattr(tc, "stdin") and tc.stdin:
                ex_lines.append(f"Example {idx} Input: {tc.stdin.strip()} -> Expected Output: {tc.expected_stdout.strip() if tc.expected_stdout else ''}")
        return "\n".join(ex_lines)

    def solve(self, problem: PublicProblem) -> SearchResult:
        tree = Tree.create_root(problem.problem_id)
        archive = CandidateArchive()
        budget = BudgetManager(self.budget_limits)

        public_examples_str = self._format_public_examples(problem)
        mode = problem.execution_spec.mode.value if hasattr(problem.execution_spec.mode, "value") else str(problem.execution_spec.mode)
        entry_point = problem.execution_spec.entry_point or "solution"

        # -------------------------------------------------------------
        # Node 1: Analyze Node (Problem Spec, Constraints, Edge Cases)
        # -------------------------------------------------------------
        budget.record_model_call("analysis")
        t_analyze = self.env.get_template("graph_analyze.jinja")
        prompt_analyze = t_analyze.render(
            statement=problem.statement,
            public_examples=public_examples_str
        )
        analysis_text = self._call_llm(prompt_analyze, role="analysis", temperature=0.1, max_tokens=600)

        # -------------------------------------------------------------
        # Node 2: Multi-Draft Node (Branching: Strategy A & B)
        # -------------------------------------------------------------
        budget.record_model_call("drafts")
        t_drafts = self.env.get_template("graph_drafts.jinja")
        prompt_drafts = t_drafts.render(
            statement=problem.statement,
            public_examples=public_examples_str,
            analysis=analysis_text,
            mode=mode,
            entry_point=entry_point
        )
        drafts_raw = self._call_llm(prompt_drafts, role="drafts", temperature=0.5, max_tokens=1536)
        draft_a, draft_b = extract_draft_codeblocks(drafts_raw)

        # -------------------------------------------------------------
        # Node 3: Aggregate Node (GoT Merge Operator)
        # -------------------------------------------------------------
        budget.record_code_generation_attempt()
        budget.record_model_call("code")
        t_aggregate = self.env.get_template("graph_aggregate.jinja")
        prompt_aggregate = t_aggregate.render(
            statement=problem.statement,
            public_examples=public_examples_str,
            analysis=analysis_text,
            draft_a=draft_a,
            draft_b=draft_b,
            mode=mode,
            entry_point=entry_point
        )
        merged_raw = self._call_llm(prompt_aggregate, role="code", temperature=0.2, max_tokens=1536)
        merged_code = extract_robust_code(merged_raw)

        cand_merged = ProgramCandidate(
            candidate_id=f"cand_graph_merged_{uuid.uuid4().hex[:6]}",
            problem_id=problem.problem_id,
            code=merged_code,
            code_hash=ProgramCandidate.compute_hash(merged_code),
            origin=CandidateOrigin.BASELINE,
            created_sequence=1
        )
        eval_rec = self.evaluator.evaluate_public(cand_merged, problem, budget=budget)
        archive.add(cand_merged, eval_rec)

        current_candidate = cand_merged
        current_eval = eval_rec
        stop_reason = "graph_aggregate_completed"

        if eval_rec.execution_summary and eval_rec.execution_summary.all_passed:
            stop_reason = "graph_aggregate_passed"
        else:
            # ---------------------------------------------------------
            # Node 5: Targeted Diagnosis & Patching Loop
            # ---------------------------------------------------------
            t_patch = self.env.get_template("graph_patch.jinja")
            for patch_i in range(self.max_patches):
                if not budget.can_start_code_generation():
                    stop_reason = "graph_budget_exhausted"
                    break

                # Extract failure feedback
                feedback_lines = []
                es = current_eval.execution_summary
                if es:
                    feedback_lines.append(f"Passed: {es.passed}/{es.total} public tests (pass rate: {es.pass_rate})")
                    if es.first_failed_case:
                        ffc = es.first_failed_case
                        feedback_lines.append(f"Failed Case ID: {ffc.case_id} (Status: {ffc.status})")
                        if ffc.error_message:
                            feedback_lines.append(f"Traceback / Error Details:\n{ffc.error_message.strip()}")
                        if ffc.expected_output is not None and ffc.actual_output is not None:
                            feedback_lines.append(f"Expected:\n{ffc.expected_output.strip()}")
                            feedback_lines.append(f"Actual:\n{ffc.actual_output.strip()}")
                feedback_text = "\n".join(feedback_lines) if feedback_lines else "Code failed some public assertions."

                budget.record_code_generation_attempt()
                budget.record_model_call("code")
                prompt_patch = t_patch.render(
                    statement=problem.statement,
                    analysis=analysis_text,
                    current_code=current_candidate.code,
                    feedback_text=feedback_text,
                    mode=mode,
                    entry_point=entry_point
                )
                patched_raw = self._call_llm(prompt_patch, role="code", temperature=0.2, max_tokens=1536)
                patched_code = extract_robust_code(patched_raw)

                cand_patched = ProgramCandidate(
                    candidate_id=f"cand_graph_patch_{patch_i+1}_{uuid.uuid4().hex[:6]}",
                    problem_id=problem.problem_id,
                    code=patched_code,
                    code_hash=ProgramCandidate.compute_hash(patched_code),
                    origin=CandidateOrigin.RETHINK,
                    created_sequence=patch_i + 2
                )
                eval_rec_patch = self.evaluator.evaluate_public(cand_patched, problem, budget=budget)
                archive.add(cand_patched, eval_rec_patch)

                current_candidate = cand_patched
                current_eval = eval_rec_patch

                if eval_rec_patch.execution_summary and eval_rec_patch.execution_summary.all_passed:
                    stop_reason = f"graph_patch_{patch_i+1}_passed"
                    break
                else:
                    stop_reason = f"graph_patch_{patch_i+1}_failed"

        # Final Selection: pick candidate with maximum reward
        selector = FinalSelectionPolicy(mode="max_reward")
        selected = selector.select(archive.entries)
        best_pair = archive.get_best()
        best_reward = best_pair[1].reward if best_pair and best_pair[1].reward is not None else 0.0

        budget.update_wall_time()
        return SearchResult(
            problem_id=problem.problem_id,
            selected_candidate=selected,
            best_reward=best_reward,
            tree=tree,
            archive=archive,
            usage=budget.usage,
            stop_reason=stop_reason
        )
