"""
Unit tests U01 to U13 verifying mathematical formulas, contracts, and policies.
"""

import math
import pytest
from rethink_mcts.policies.selection import PUCBSelector
from rethink_mcts.policies.backup import MaxBackupPolicy
from rethink_mcts.policies.reward import PaperDualRewardPolicy
from rethink_mcts.policies.prior import PriorPolicy
from rethink_mcts.policies.final_selection import FinalSelectionPolicy
from rethink_mcts.domain.candidate import (
    ProgramCandidate,
    EvaluationRecord,
    ExecutionSummary,
    SingleCaseResult,
    CandidateVerdict
)
from rethink_mcts.domain.tree import Tree, ThoughtProposal, SearchNode, NodeStatus


def test_u01_p_ucb_exact_computation():
    """
    U01: P-UCB với N(parent)=10, N(child)=2, P=.4, Q=.5, c_base=10, c=4
    Score ≈ 1.459405916364923, tolerance 1e-12.
    """
    selector = PUCBSelector(c_base=10.0, c=4.0)
    score = selector.compute_score(
        parent_visits=10,
        child_visits=2,
        prior=0.4,
        q_value=0.5
    )
    expected = 1.459405916364923
    assert abs(score - expected) < 1e-12, f"Expected {expected}, got {score}"


def test_u02_unvisited_siblings_bootstrap():
    """
    U02: N(parent)=0; unvisited siblings -> Không NaN/log(0), chọn prior cao nhất.
    """
    tree = Tree.create_root("prob1")
    root = tree.get_node(tree.root_id)
    root.visits = 0

    p1 = ThoughtProposal("Th1", raw_reasonableness=0.3, normalized_prior=0.3)
    p2 = ThoughtProposal("Th2", raw_reasonableness=0.7, normalized_prior=0.7)
    tree.create_child_node(root.node_id, p1, parent_path_hash="root")
    tree.create_child_node(root.node_id, p2, parent_path_hash="root")

    selector = PUCBSelector(c_base=10.0, c=4.0)
    best_child = selector.select_best_child(tree, root)
    assert best_child is not None
    assert best_child.prior == 0.7
    assert not math.isnan(best_child.prior)


def test_u03_max_backup_vs_mean():
    """
    U03: Hai rewards .2 và .8 -> visits=2, Q=.8, không phải .5.
    """
    tree = Tree.create_root("prob1")
    root = tree.get_node(tree.root_id)
    p = ThoughtProposal("Th", raw_reasonableness=1.0, normalized_prior=1.0)
    child = tree.create_child_node(root.node_id, p, parent_path_hash="root")

    backup = MaxBackupPolicy()
    backup.backup(tree, child.node_id, reward=0.2, evaluation_id="eval_1")
    backup.backup(tree, child.node_id, reward=0.8, evaluation_id="eval_2")

    assert child.visits == 2
    assert child.q_max == 0.8
    assert root.visits == 2
    assert root.q_max == 0.8


def test_u04_v_test_partial_critic_skipped():
    """
    U04: v_test=.5 -> r=.5, critic không được gọi.
    """
    reward_policy = PaperDualRewardPolicy(test_weight=0.8, llm_weight=0.2)
    summary = ExecutionSummary(
        total=2,
        executed=2,
        passed=1,
        failed=1,
        pass_rate=0.5,
        all_passed=False
    )
    assert not reward_policy.should_call_critic(summary)
    reward = reward_policy.compute_reward(summary, v_llm=0.9)
    assert reward == 0.5


def test_u05_public_full_pass_reference_critic_range():
    """
    U05: Public full pass, critic=-1, reference ([-1, 1]) -> r=0.6.
    a*1.0 + b*(-1.0) = 0.8 - 0.2 = 0.6.
    """
    reward_policy = PaperDualRewardPolicy(test_weight=0.8, llm_weight=0.2, critic_min=-1.0, critic_max=1.0)
    summary = ExecutionSummary(
        total=2,
        executed=2,
        passed=2,
        failed=0,
        pass_rate=1.0,
        all_passed=True
    )
    assert reward_policy.should_call_critic(summary)
    reward = reward_policy.compute_reward(summary, v_llm=-1.0)
    assert abs(reward - 0.6) < 1e-12


def test_u06_public_full_pass_compact_critic_range():
    """
    U06: Public full pass, critic=.5, compact ([0, 1]) -> r=0.9.
    a*1.0 + b*(0.5) = 0.8 + 0.1 = 0.9.
    """
    reward_policy = PaperDualRewardPolicy(test_weight=0.8, llm_weight=0.2, critic_min=0.0, critic_max=1.0)
    summary = ExecutionSummary(
        total=2,
        executed=2,
        passed=2,
        failed=0,
        pass_rate=1.0,
        all_passed=True
    )
    reward = reward_policy.compute_reward(summary, v_llm=0.5)
    assert abs(reward - 0.9) < 1e-12


def test_u07_no_clamping_on_extended_weights():
    """
    U07: a=1, b=1, critic=1 -> r=2, không clamp.
    """
    reward_policy = PaperDualRewardPolicy(test_weight=1.0, llm_weight=1.0)
    summary = ExecutionSummary(total=1, executed=1, passed=1, failed=0, pass_rate=1.0, all_passed=True)
    reward = reward_policy.compute_reward(summary, v_llm=1.0)
    assert reward == 2.0


def test_u08_empty_public_suite_no_tests():
    """
    U08: Public suite rỗng -> NO_TESTS, pass_rate=None, all_passed=False.
    """
    summary = ExecutionSummary.empty()
    assert summary.total == 0
    assert summary.pass_rate is None
    assert summary.all_passed is False
    reward_policy = PaperDualRewardPolicy()
    assert reward_policy.compute_reward(summary) is None


def test_u09_prior_normalization():
    """
    U09: Priors 2/3/5 -> Normalize theo policy: 0.2, 0.3, 0.5.
    """
    policy = PriorPolicy()
    proposals = policy.process_raw_proposals([
        ("Strategy 1", 2.0),
        ("Strategy 2", 3.0),
        ("Strategy 3", 5.0)
    ])
    priors = [p.normalized_prior for p in proposals]
    assert abs(priors[0] - 0.2) < 1e-12
    assert abs(priors[1] - 0.3) < 1e-12
    assert abs(priors[2] - 0.5) < 1e-12
    assert abs(sum(priors) - 1.0) < 1e-12


def test_u10_prior_fallback_uniform_on_zero_total():
    """
    U10: NaN/negative/zero-total scores -> fallback uniform.
    """
    policy = PriorPolicy(fallback_mode="uniform_after_retry")
    proposals = policy.process_raw_proposals([
        ("Strategy A", 0.0),
        ("Strategy B", 0.0)
    ])
    assert len(proposals) == 2
    assert proposals[0].normalized_prior == 0.5
    assert proposals[1].normalized_prior == 0.5


def test_u11_thought_dedup_and_mass_aggregation():
    """
    U11: Thought trùng batch -> Dedup, cộng mass, renormalize, creation order ổn định.
    """
    policy = PriorPolicy()
    proposals = policy.process_raw_proposals([
        ("Use DFS", 0.4),
        ("use dfs", 0.3),  # Duplicate of first
        ("Use BFS", 0.3)
    ])
    assert len(proposals) == 2
    assert proposals[0].text == "Use DFS" or proposals[0].text.lower() == "use dfs"
    assert abs(proposals[0].raw_reasonableness - 0.7) < 1e-12
    assert abs(proposals[0].normalized_prior - 0.7) < 1e-12
    assert abs(proposals[1].normalized_prior - 0.3) < 1e-12


def test_u12_final_selection_from_archive():
    """
    U12: Final selection có code cũ tốt hơn code mới -> Chọn từ archive, không chỉ active leaf.
    """
    c1 = ProgramCandidate("c1", "p", "old_good_code", "h1", created_sequence=1)
    e1 = EvaluationRecord("e1", "c1", reward=0.95)

    c2 = ProgramCandidate("c2", "p", "new_worse_code", "h2", created_sequence=2)
    e2 = EvaluationRecord("e2", "c2", reward=0.40)

    selector = FinalSelectionPolicy(mode="max_reward")
    selected = selector.select([(c1, e1), (c2, e2)])
    assert selected is not None
    assert selected.candidate_id == "c1"


def test_u13_max_reward_vs_public_first():
    """
    U13: Public-full candidate r=.8, partial candidate r=.9.
    max_reward chọn partial (0.9); public-first chọn full (0.8).
    """
    c_full = ProgramCandidate("c_full", "p", "full_pass_code", "h_f", created_sequence=1)
    e_full = EvaluationRecord(
        "e_full", "c_full", reward=0.8,
        execution_summary=ExecutionSummary(1, 1, 1, 0, 1.0, True)
    )

    c_part = ProgramCandidate("c_part", "p", "partial_code", "h_p", created_sequence=2)
    e_part = EvaluationRecord(
        "e_part", "c_part", reward=0.9,
        execution_summary=ExecutionSummary(2, 2, 1, 1, 0.5, False)
    )

    archive = [(c_full, e_full), (c_part, e_part)]

    # 1. max_reward mode
    max_sel = FinalSelectionPolicy(mode="max_reward")
    assert max_sel.select(archive).candidate_id == "c_part"

    # 2. public_first_then_reward mode
    pub_first_sel = FinalSelectionPolicy(mode="public_first_then_reward")
    assert pub_first_sel.select(archive).candidate_id == "c_full"
