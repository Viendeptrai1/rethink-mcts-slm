"""
Contract tests I04 to I11 verifying Tree, Leaf Revision, Ancestor Accounting, and Budget boundaries.
"""

import pytest
from rethink_mcts.domain.tree import Tree, ThoughtProposal, NodeStatus
from rethink_mcts.policies.backup import MaxBackupPolicy
from rethink_mcts.domain.candidate import ProgramCandidate, CandidateOrigin
from rethink_mcts.domain.budget import BudgetLimits, BudgetManager
from rethink_mcts.application.search import SearchEngine
from rethink_mcts.adapters.llm.mock import ScenarioMockLLM
from rethink_mcts.adapters.execution.trusted_fixture_executor import TrustedFixtureExecutor
from rethink_mcts.application.evaluate import CandidateEvaluator
from rethink_mcts.application.feedback import FeedbackService
from rethink_mcts.policies.selection import PUCBSelector
from rethink_mcts.policies.reward import PaperDualRewardPolicy
from rethink_mcts.policies.stopping import StoppingPolicy
from rethink_mcts.policies.final_selection import FinalSelectionPolicy
from rethink_mcts.domain.problem import PublicProblem, StdinCase, ExecutionSpec


def test_i04_rethink_leaf_reset_and_ancestor_receives_both():
    """
    I04: Rethink .4 -> .9. Leaf revision reset rồi N=1/Q=.9; ancestor nhận cả 2 evaluations (visits=2, Q=.9).
    """
    tree = Tree.create_root("prob1")
    root = tree.get_node(tree.root_id)
    p = ThoughtProposal("Naive thought", 0.5, 0.5)
    leaf = tree.create_child_node(root.node_id, p, parent_path_hash="root")

    backup = MaxBackupPolicy()
    # 1. Initial evaluation with reward 0.4
    backup.backup(tree, leaf.node_id, reward=0.4, evaluation_id="eval_1")
    assert leaf.visits == 1
    assert leaf.q_max == 0.4
    assert root.visits == 1
    assert root.q_max == 0.4

    # 2. Leaf revision
    new_rev = tree.begin_leaf_revision(leaf.node_id, "Corrected thought")
    assert leaf.active_revision_id == new_rev.revision_id
    assert leaf.visits == 0  # Reset for new revision
    assert leaf.q_max == 0.0

    # 3. Evaluate new revision with reward 0.9
    backup.backup(tree, leaf.node_id, reward=0.9, evaluation_id="eval_2")
    assert leaf.visits == 1
    assert leaf.q_max == 0.9
    # Ancestor holds all historical evaluations of prefix
    assert root.visits == 2
    assert root.q_max == 0.9


def test_i05_rethink_lower_reward_keeps_ancestor_max():
    """
    I05: Rethink .9 -> .2. Active revision Q=.2; ancestor giữ .9.
    """
    tree = Tree.create_root("prob1")
    root = tree.get_node(tree.root_id)
    leaf = tree.create_child_node(root.node_id, ThoughtProposal("Th1", 0.5, 0.5), "root")

    backup = MaxBackupPolicy()
    backup.backup(tree, leaf.node_id, reward=0.9, evaluation_id="eval_1")
    assert root.q_max == 0.9

    tree.begin_leaf_revision(leaf.node_id, "Worse thought")
    backup.backup(tree, leaf.node_id, reward=0.2, evaluation_id="eval_2")

    assert leaf.q_max == 0.2
    assert root.q_max == 0.9  # Max preserved!


def test_i06_rethink_rejects_node_with_children():
    """
    I06: Node có children không được phép rethink (invariant §7.5).
    """
    tree = Tree.create_root("prob1")
    root = tree.get_node(tree.root_id)
    parent_node = tree.create_child_node(root.node_id, ThoughtProposal("P", 0.5, 0.5), "root")
    # Add child to parent_node
    tree.create_child_node(parent_node.node_id, ThoughtProposal("Child", 0.5, 0.5), "p")

    with pytest.raises(ValueError) as exc:
        tree.begin_leaf_revision(parent_node.node_id, "Illegal revision")
    assert "already has children" in str(exc.value)


def test_i08_parent_path_preserves_all_ancestor_thoughts():
    """
    I08: Parent path có 3 thoughts -> trích xuất đủ 3 thoughts, không cắt bớt.
    """
    tree = Tree.create_root("prob1")
    r = tree.root_id
    n1 = tree.create_child_node(r, ThoughtProposal("Thought 1", 1.0, 1.0), "r")
    n2 = tree.create_child_node(n1.node_id, ThoughtProposal("Thought 2", 1.0, 1.0), "n1")
    n3 = tree.create_child_node(n2.node_id, ThoughtProposal("Thought 3", 1.0, 1.0), "n2")
    leaf = tree.create_child_node(n3.node_id, ThoughtProposal("Leaf Thought", 1.0, 1.0), "n3")

    parent_thoughts = tree.get_active_thought_path_to_parent(leaf.node_id)
    assert len(parent_thoughts) == 3
    assert parent_thoughts == ("Thought 1", "Thought 2", "Thought 3")


def test_i10_strict_budget_cutoff_stops_generation():
    """
    I10: Budget max_code_generations=1 -> Search halts without exceeding 1 code attempt.
    """
    problem = PublicProblem(
        problem_id="p_budget",
        statement="Problem statement",
        execution_spec=ExecutionSpec(),
        public_tests=(StdinCase("1", "2"),)
    )
    mock = ScenarioMockLLM()
    executor = TrustedFixtureExecutor()
    evaluator = CandidateEvaluator(executor, mock, PaperDualRewardPolicy())
    feedback_service = FeedbackService(mode="none")
    limits = BudgetLimits(max_code_generations=1, max_model_calls=10, max_search_iterations=10)

    engine = SearchEngine(
        proposer=mock,
        generator=mock,
        refiner=mock,
        evaluator=evaluator,
        feedback_service=feedback_service,
        selector=PUCBSelector(),
        backup_policy=MaxBackupPolicy(),
        stopping_policy=StoppingPolicy(max_depth=2),
        final_selector=FinalSelectionPolicy(),
        budget_limits=limits,
        width=2,
        max_depth=2,
        max_rethinks_per_node=1
    )
    res = engine.solve(problem)
    assert res.usage.code_generation_attempts <= 1
