"""
Baseline implementations for comparison matching §16 of RethinkMCTS spec.
All baselines adhere to the same PublicProblem contract and budget accounting.
"""

import uuid
from rethink_mcts.application.model_calls import invoke_model
from rethink_mcts.domain.errors import (
    BudgetExceededError,
    GenerationTruncatedError,
    InvalidModelOutputError,
)
from typing import Optional
from rethink_mcts.domain.problem import PublicProblem
from rethink_mcts.domain.candidate import ProgramCandidate, CandidateOrigin
from rethink_mcts.domain.tree import Tree
from rethink_mcts.domain.budget import BudgetLimits, BudgetManager
from rethink_mcts.ports.models import ThoughtProposer, CodeGenerator
from rethink_mcts.policies.final_selection import FinalSelectionPolicy
from rethink_mcts.application.candidate_archive import CandidateArchive
from rethink_mcts.application.evaluate import CandidateEvaluator
from rethink_mcts.application.search import SearchResult


class DirectBaseline:
    """Direct generation: 1 single code generation, no tree, no feedback loop (§16)."""
    def __init__(
        self,
        generator: CodeGenerator,
        evaluator: CandidateEvaluator,
        budget_limits: BudgetLimits
    ):
        self.generator = generator
        self.evaluator = evaluator
        self.budget_limits = budget_limits

    def solve(self, problem: PublicProblem) -> SearchResult:
        tree = Tree.create_root(problem.problem_id)
        archive = CandidateArchive()
        budget = BudgetManager(self.budget_limits)
        self.last_budget = budget

        budget.record_code_generation_attempt()
        try:
            code = invoke_model(budget, self.generator, "generate", "code",
                statement=problem.statement,
                execution_spec=problem.execution_spec,
                active_thoughts=()
            )
        except (InvalidModelOutputError, GenerationTruncatedError) as exc:
            code = f"# Code generation failed or truncated: {exc}"

        candidate = ProgramCandidate(
            candidate_id=f"cand_dir_{uuid.uuid4().hex[:8]}",
            problem_id=problem.problem_id,
            code=code,
            code_hash=ProgramCandidate.compute_hash(code),
            origin=CandidateOrigin.BASELINE,
            created_sequence=1
        )

        eval_rec = self.evaluator.evaluate_public(candidate, problem, budget=budget)
        archive.add(candidate, eval_rec)

        budget.update_wall_time()
        return SearchResult(
            problem_id=problem.problem_id,
            selected_candidate=candidate,
            best_reward=eval_rec.reward if eval_rec.reward is not None else 0.0,
            tree=tree,
            archive=archive,
            usage=budget.usage,
            request_records=tuple(budget.requests),
            stop_reason="direct_completed"
        )


class BestOfNPublicBaseline:
    """Best-of-N: N independent candidates evaluated on public suite (§16)."""
    def __init__(
        self,
        generator: CodeGenerator,
        evaluator: CandidateEvaluator,
        budget_limits: BudgetLimits,
        n: int = 4
    ):
        self.generator = generator
        self.evaluator = evaluator
        self.budget_limits = budget_limits
        self.n = n

    def solve(self, problem: PublicProblem) -> SearchResult:
        tree = Tree.create_root(problem.problem_id)
        archive = CandidateArchive()
        budget = BudgetManager(self.budget_limits)
        self.last_budget = budget

        for i in range(self.n):
            if not budget.can_start_code_generation():
                break

            budget.record_code_generation_attempt()
            try:
                code = invoke_model(budget, self.generator, "generate", "code",
                    statement=problem.statement,
                    execution_spec=problem.execution_spec,
                    active_thoughts=()
                )
            except (InvalidModelOutputError, GenerationTruncatedError) as exc:
                code = f"# Code generation failed or truncated: {exc}"

            candidate = ProgramCandidate(
                candidate_id=f"cand_bon_{i}_{uuid.uuid4().hex[:6]}",
                problem_id=problem.problem_id,
                code=code,
                code_hash=ProgramCandidate.compute_hash(code),
                origin=CandidateOrigin.BASELINE,
                created_sequence=i + 1
            )
            eval_rec = self.evaluator.evaluate_public(candidate, problem, budget=budget)
            archive.add(candidate, eval_rec)

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
            request_records=tuple(budget.requests),
            stop_reason="best_of_n_completed"
        )


class IterativeRepairBaseline:
    """Generate once, then repair code directly with public feedback; no tree search."""
    def __init__(self, generator, evaluator, budget_limits, feedback_service):
        self.generator, self.evaluator = generator, evaluator
        self.budget_limits, self.feedback_service = budget_limits, feedback_service

    def solve(self, problem):
        tree, archive = Tree.create_root(problem.problem_id), CandidateArchive()
        budget = BudgetManager(self.budget_limits)
        self.last_budget = budget
        self.feedback_service.reset()
        candidate = evaluation = None
        stop_reason = "budget_exhausted"
        try:
            while budget.can_start_code_generation():
                try:
                    if candidate is None:
                        budget.record_code_generation_attempt()
                        code = invoke_model(budget, self.generator, "generate", "code",
                            statement=problem.statement, execution_spec=problem.execution_spec, active_thoughts=())
                    else:
                        feedback = self.feedback_service.build_feedback(candidate, evaluation, problem,
                                                                       budget, reserved_model_calls=1)
                        budget.record_code_generation_attempt()
                        code = invoke_model(budget, self.generator, "repair", "code",
                            statement=problem.statement, execution_spec=problem.execution_spec,
                            candidate_code=candidate.code, feedback=feedback)
                except (InvalidModelOutputError, GenerationTruncatedError) as exc:
                    code = f"# Code generation failed or truncated: {exc}"
                candidate = ProgramCandidate(
                    candidate_id=f"cand_repair_{uuid.uuid4().hex[:8]}", problem_id=problem.problem_id,
                    code=code, code_hash=ProgramCandidate.compute_hash(code),
                    origin=CandidateOrigin.BASELINE, created_sequence=budget.usage.code_generation_attempts)
                evaluation = self.evaluator.evaluate_public(candidate, problem, budget)
                archive.add(candidate, evaluation)
                if evaluation.execution_summary.all_passed:
                    stop_reason = "public_all_passed"
                    break
        except BudgetExceededError as exc:
            stop_reason = str(exc)
        selected = FinalSelectionPolicy().select(archive.entries)
        best = archive.get_best()
        budget.update_wall_time()
        return SearchResult(problem.problem_id, selected, best[1].reward if best else 0.0,
                            tree, archive, budget.usage, stop_reason,
                            tuple(budget.requests), tuple(self.feedback_service.records))
