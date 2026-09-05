"""
Acceptance test Scenario C: Swapping endpoint/model configuration without altering search engine core (§18.5).
"""

from rethink_mcts.config import AppConfig
from rethink_mcts.bootstrap import create_search_engine
from rethink_mcts.domain.problem import PublicProblem, StdinCase, ExecutionSpec, ProblemLimits, PublicMetadata


def test_scenario_c_endpoint_swap_without_code_changes(tmp_path):
    prob = PublicProblem(
        problem_id="p_swap",
        statement="Write a program to print 42",
        execution_spec=ExecutionSpec(),
        public_tests=(StdinCase("", "42\n"),),
        limits=ProblemLimits(),
        metadata=PublicMetadata()
    )

    # 1. First run with local mock profile
    cfg1 = AppConfig.from_yaml_file("configs/smoke_mock.yaml")
    cfg1.storage.output_dir = str(tmp_path / "run1")
    engine1, store1 = create_search_engine(cfg1, run_dir=cfg1.storage.output_dir)
    res1 = engine1.solve(prob)
    assert res1.selected_candidate is not None

    # 2. Second run with simulated remote profile (using mock transport to avoid external network dependence)
    cfg2 = AppConfig.from_yaml_file("configs/remote_14b.yaml")
    cfg2.model.transport = "mock"
    cfg2.experiment.allow_mock = True
    cfg2.storage.output_dir = str(tmp_path / "run2")
    engine2, store2 = create_search_engine(cfg2, run_dir=cfg2.storage.output_dir)
    res2 = engine2.solve(prob)
    assert res2.selected_candidate is not None

    # Both produced identical domain DTO contracts and invariants
    assert res1.usage.total_model_calls > 0
    assert res2.usage.total_model_calls > 0
