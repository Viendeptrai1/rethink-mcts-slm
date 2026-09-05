"""
Acceptance test Scenario D: Budget enforcement and checkpoint persistence (§18.6).
"""

import os
import json
from rethink_mcts.domain.problem import PublicProblem, StdinCase, ExecutionSpec, ProblemLimits, PublicMetadata
from rethink_mcts.domain.budget import BudgetLimits
from rethink_mcts.domain.candidate import CandidateOrigin
from rethink_mcts.adapters.llm.mock import ScenarioMockLLM
from rethink_mcts.adapters.execution.trusted_fixture_executor import TrustedFixtureExecutor
from rethink_mcts.adapters.storage.filesystem import FileSystemRunStore
from rethink_mcts.application.evaluate import CandidateEvaluator
from rethink_mcts.application.feedback import FeedbackService
from rethink_mcts.application.search import SearchEngine
from rethink_mcts.policies.selection import PUCBSelector
from rethink_mcts.policies.backup import MaxBackupPolicy
from rethink_mcts.policies.reward import PaperDualRewardPolicy
from rethink_mcts.policies.stopping import StoppingPolicy
from rethink_mcts.policies.final_selection import FinalSelectionPolicy


def test_scenario_d_budget_cap_and_checkpoint(tmp_path):
    prob = PublicProblem(
        problem_id="watermelon_budget",
        statement="Watermelon even division problem",
        execution_spec=ExecutionSpec(),
        public_tests=(
            StdinCase("8\n", "YES\n"),
            StdinCase("2\n", "NO\n")
        ),
        limits=ProblemLimits(),
        metadata=PublicMetadata()
    )

    mock = ScenarioMockLLM()
    executor = TrustedFixtureExecutor()
    evaluator = CandidateEvaluator(executor, mock, PaperDualRewardPolicy())
    feedback = FeedbackService(mode="block", block_analyzer=mock)

    # Budget strictly set to 2 code generations
    budget_limits = BudgetLimits(max_code_generations=2, max_model_calls=10, max_search_iterations=10)

    run_dir = str(tmp_path / "run_d")
    store = FileSystemRunStore(run_dir=run_dir)

    engine = SearchEngine(
        proposer=mock,
        generator=mock,
        refiner=mock,
        evaluator=evaluator,
        feedback_service=feedback,
        selector=PUCBSelector(),
        backup_policy=MaxBackupPolicy(),
        stopping_policy=StoppingPolicy(max_depth=3),
        final_selector=FinalSelectionPolicy(),
        budget_limits=budget_limits,
        width=2,
        max_depth=3,
        max_rethinks_per_node=1
    )

    res = engine.solve(prob)

    # Assert: Exactly 2 code generations occurred (initial + 1 rethink), not 3!
    assert res.usage.code_generation_attempts == 2

    # Save checkpoint
    store.save_checkpoint(prob.problem_id, res.tree, res.selected_candidate.candidate_id if res.selected_candidate else None)
    checkpoint_file = os.path.join(run_dir, "problems", prob.problem_id, "checkpoint.json")
    assert os.path.exists(checkpoint_file)

    with open(checkpoint_file, "r") as f:
        cp_data = json.load(f)
    assert cp_data["root_id"] == "root"
    assert len(cp_data["nodes"]) >= 2
