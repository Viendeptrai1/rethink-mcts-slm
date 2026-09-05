"""
SearchEngine orchestrating Thought-Level MCTS with Leaf Revision lifecycle matching §7 of spec.
"""

import uuid
import logging
from dataclasses import dataclass
from typing import Optional

from rethink_mcts.domain.problem import PublicProblem
from rethink_mcts.domain.tree import Tree, NodeStatus, CloseReason
from rethink_mcts.domain.candidate import ProgramCandidate, CandidateOrigin
from rethink_mcts.domain.budget import BudgetLimits, BudgetManager, Usage
from rethink_mcts.domain.errors import NoTestsError
from rethink_mcts.ports.models import ThoughtProposer, CodeGenerator, ThoughtRefiner
from rethink_mcts.policies.selection import PUCBSelector
from rethink_mcts.policies.prior import PriorPolicy
from rethink_mcts.policies.backup import MaxBackupPolicy
from rethink_mcts.policies.stopping import StoppingPolicy
from rethink_mcts.policies.final_selection import FinalSelectionPolicy
from rethink_mcts.application.candidate_archive import CandidateArchive
from rethink_mcts.application.evaluate import CandidateEvaluator
from rethink_mcts.application.feedback import FeedbackService

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SearchResult:
    problem_id: str
    selected_candidate: Optional[ProgramCandidate]
    best_reward: float
    tree: Tree
    archive: CandidateArchive
    usage: Usage
    stop_reason: str


class SearchEngine:
    def __init__(
        self,
        proposer: ThoughtProposer,
        generator: CodeGenerator,
        refiner: ThoughtRefiner,
        evaluator: CandidateEvaluator,
        feedback_service: FeedbackService,
        selector: PUCBSelector,
        backup_policy: MaxBackupPolicy,
        stopping_policy: StoppingPolicy,
        final_selector: FinalSelectionPolicy,
        budget_limits: BudgetLimits,
        width: int = 3,
        max_depth: int = 4,
        max_rethinks_per_node: int = 1
    ):
        self.proposer = proposer
        self.generator = generator
        self.refiner = refiner
        self.evaluator = evaluator
        self.feedback_service = feedback_service
        self.selector = selector
        self.backup_policy = backup_policy
        self.stopping_policy = stopping_policy
        self.final_selector = final_selector
        self.budget_limits = budget_limits
        self.width = width
        self.max_depth = max_depth
        self.max_rethinks_per_node = max_rethinks_per_node

    def solve(self, problem: PublicProblem) -> SearchResult:
        """
        Executes complete search algorithm lifecycle on PublicProblem.
        """
        if not problem.public_tests:
            raise NoTestsError(f"PublicProblem '{problem.problem_id}' has no public tests")

        tree = Tree.create_root(problem.problem_id)
        archive = CandidateArchive()
        budget = BudgetManager(self.budget_limits)
        seq_counter = 0

        # 1. Expand root once to bootstrap initial thoughts (§7.2 step 1)
        budget.record_model_call("expansion")
        root_proposals = self.proposer.propose(
            statement=problem.statement,
            active_thoughts=(),
            width=self.width,
            feedback=None
        )
        logger.info("Bootstrap: Root expanded with %d initial thought proposals", len(root_proposals.proposals))
        for p in root_proposals.proposals:
            logger.info("  -> Proposal [prior=%.2f]: %s", p.normalized_prior, p.text)
            tree.create_child_node(tree.root_id, p, parent_path_hash="root")

        stop_reason = "normal"

        # 2. Main MCTS search loop
        while budget.can_start_code_generation():
            should_stop, reason = self.stopping_policy.should_stop(tree, budget)
            if should_stop:
                stop_reason = reason
                break

            # Selection: traverse from root down to frontier
            curr = tree.get_node(tree.root_id)
            while curr.child_ids and curr.status == NodeStatus.READY:
                next_child = self.selector.select_best_child(tree, curr)
                if next_child is None:
                    break
                curr = next_child

            node = curr
            logger.info("Selected node %s (depth=%d, status=%s)", node.node_id, node.depth, node.status.value)

            # If node is READY and can expand children
            if node.status == NodeStatus.READY:
                if node.depth >= self.max_depth:
                    node.mark_closed(CloseReason.DEPTH_LIMIT)
                    continue

                active_thoughts = tree.get_active_thought_path(node.node_id)
                budget.record_model_call("expansion")
                proposals = self.proposer.propose(
                    statement=problem.statement,
                    active_thoughts=active_thoughts,
                    width=self.width,
                    feedback=None
                )
                if not proposals.proposals:
                    node.mark_closed(CloseReason.NO_VALID_PROPOSALS)
                    continue

                parent_hash = str(hash(active_thoughts))
                for p in proposals.proposals:
                    tree.create_child_node(node.node_id, p, parent_path_hash=parent_hash)
                continue

            # If node is UNEVALUATED, evaluate candidate program
            if node.status == NodeStatus.UNEVALUATED:
                node.status = NodeStatus.EVALUATING
                active_thoughts = tree.get_active_thought_path(node.node_id)

                # Generate code
                budget.record_code_generation_attempt()
                budget.record_model_call("code")
                logger.info("Generating candidate code for node %s with thoughts: %s", node.node_id, active_thoughts)
                code = self.generator.generate(
                    statement=problem.statement,
                    execution_spec=problem.execution_spec,
                    active_thoughts=active_thoughts
                )

                seq_counter += 1
                candidate = ProgramCandidate(
                    candidate_id=f"cand_{uuid.uuid4().hex[:10]}",
                    problem_id=problem.problem_id,
                    code=code,
                    code_hash=ProgramCandidate.compute_hash(code),
                    node_id=node.node_id,
                    revision_id=node.active_revision_id,
                    thought_path_snapshot=active_thoughts,
                    origin=CandidateOrigin.INITIAL,
                    created_sequence=seq_counter
                )

                # Evaluate on public suite
                evaluation = self.evaluator.evaluate_public(candidate, problem, budget=budget)
                archive.add(candidate, evaluation)
                logger.info(
                    "Candidate %s evaluated: %d/%d passed, reward=%.3f",
                    candidate.candidate_id,
                    evaluation.execution_summary.passed,
                    evaluation.execution_summary.total,
                    evaluation.reward or 0.0
                )

                if evaluation.reward is not None:
                    self.backup_policy.backup(
                        tree=tree,
                        leaf_node_id=node.node_id,
                        reward=evaluation.reward,
                        evaluation_id=evaluation.evaluation_id
                    )

                # Rethink Loop if public tests failed (§7.2 step 5-6)
                if not evaluation.execution_summary.all_passed:
                    for _ in range(self.max_rethinks_per_node):
                        if evaluation.execution_summary.all_passed:
                            break
                        if not budget.can_reserve_refinement_and_regeneration():
                            break

                        logger.info("Public tests failed on candidate %s! Triggering Rethink on leaf %s...", candidate.candidate_id, node.node_id)

                        # Build structured feedback
                        feedback = self.feedback_service.build_feedback(candidate, evaluation, problem)
                        node.active_feedback_id = feedback.feedback_id

                        # Refine thought
                        parent_thoughts = tree.get_active_thought_path_to_parent(node.node_id)
                        curr_rev = tree.get_revision(node.active_revision_id)

                        budget.record_model_call("rethink")
                        new_thought = self.refiner.refine(
                            statement=problem.statement,
                            execution_spec=problem.execution_spec,
                            parent_thoughts=parent_thoughts,
                            erroneous_thought=curr_rev.thought_text,
                            candidate_code=candidate.code,
                            feedback=feedback
                        )
                        logger.info("Rethink produced revised thought: %s", new_thought)

                        # Create leaf revision
                        tree.begin_leaf_revision(node.node_id, new_thought, feedback.feedback_id)

                        # Regenerate complete program
                        budget.record_code_generation_attempt()
                        budget.record_rethink_attempt()
                        budget.record_model_call("code")
                        revised_thoughts = tree.get_active_thought_path(node.node_id)
                        new_code = self.generator.generate(
                            statement=problem.statement,
                            execution_spec=problem.execution_spec,
                            active_thoughts=revised_thoughts
                        )

                        seq_counter += 1
                        candidate = ProgramCandidate(
                            candidate_id=f"cand_{uuid.uuid4().hex[:10]}",
                            problem_id=problem.problem_id,
                            code=new_code,
                            code_hash=ProgramCandidate.compute_hash(new_code),
                            node_id=node.node_id,
                            revision_id=node.active_revision_id,
                            thought_path_snapshot=revised_thoughts,
                            origin=CandidateOrigin.RETHINK,
                            created_sequence=seq_counter
                        )

                        # Evaluate regenerated candidate
                        evaluation = self.evaluator.evaluate_public(candidate, problem, budget=budget)
                        archive.add(candidate, evaluation)
                        logger.info(
                            "Regenerated candidate %s evaluated: %d/%d passed, reward=%.3f",
                            candidate.candidate_id,
                            evaluation.execution_summary.passed,
                            evaluation.execution_summary.total,
                            evaluation.reward or 0.0
                        )

                        if evaluation.reward is not None:
                            self.backup_policy.backup(
                                tree=tree,
                                leaf_node_id=node.node_id,
                                reward=evaluation.reward,
                                evaluation_id=evaluation.evaluation_id
                            )

                # Finalize node status
                if node.depth >= self.max_depth:
                    node.mark_closed(CloseReason.DEPTH_LIMIT)
                else:
                    node.status = NodeStatus.READY

        # 3. Final selection from candidate archive
        selected = self.final_selector.select(archive.entries)
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
