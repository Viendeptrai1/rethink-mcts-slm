"""Shared, configuration-driven construction for all solvers."""
import os
from pathlib import Path
from rethink_mcts.config import AppConfig
from rethink_mcts.domain.budget import BudgetLimits
from rethink_mcts.policies.selection import PUCBSelector
from rethink_mcts.policies.prior import PriorPolicy
from rethink_mcts.policies.backup import MaxBackupPolicy, MeanBackupPolicy
from rethink_mcts.policies.reward import PaperDualRewardPolicy
from rethink_mcts.policies.stopping import StoppingPolicy
from rethink_mcts.policies.final_selection import FinalSelectionPolicy
from rethink_mcts.adapters.llm.mock import ScenarioMockLLM
from rethink_mcts.adapters.llm.http_gateway import HttpModelGateway
from rethink_mcts.adapters.llm.semantic import SemanticPromptedLLM
from rethink_mcts.adapters.execution.trusted_fixture_executor import TrustedFixtureExecutor
from rethink_mcts.adapters.execution.docker_executor import DockerExecutor
from rethink_mcts.adapters.execution.tracing import DynamicTraceCollector
from rethink_mcts.adapters.storage.filesystem import FileSystemRunStore
from rethink_mcts.application.evaluate import CandidateEvaluator
from rethink_mcts.application.feedback import FeedbackService
from rethink_mcts.application.search import SearchEngine
from rethink_mcts.application.baselines import DirectBaseline, BestOfNPublicBaseline, IterativeRepairBaseline
from rethink_mcts.application.graph_solver import GraphSolver


def create_executor(config):
    if config.execution.backend == "docker":
        return DockerExecutor(image=config.execution.image, allow_host_fallback=False,
                              cpus=config.execution.cpus, pids_limit=config.execution.pids_limit)
    return TrustedFixtureExecutor(test_workers=config.execution.test_workers,
                                  max_test_processes=config.execution.max_test_processes)


def create_solver(config: AppConfig, solver_type="mcts", run_dir="runs/default", n=4):
    # Revalidate mutations made via CLI/model_copy before constructing anything.
    config = AppConfig.model_validate(config.model_dump())
    prompts_dir = str(Path(__file__).resolve().parents[2] / "prompts" / config.prompts.bundle)
    if config.model.transport == "mock":
        model = ScenarioMockLLM()
        gateway = model
    else:
        api_key = os.environ.get(config.model.api_key_env, "") if config.model.api_key_env else "ollama"
        gateway = HttpModelGateway(config.model.base_url, config.model.model, api_key,
                                   config.model.request_timeout_seconds, config.model.max_transport_retries,
                                   extra_body=config.model.extra_body)
        model = SemanticPromptedLLM(gateway=gateway, prompts_dir=prompts_dir,
            prior_policy=PriorPolicy(config.search.prior_fallback), sampling=config.sampling,
            seed=config.experiment.seed, critic_min=config.reward.critic_score_min,
            critic_max=config.reward.critic_score_max, max_prompt_blocks=config.feedback.max_prompt_blocks,
            require_exact_token_count=config.model.require_exact_token_count,
            strict_variables=config.prompts.strict_variables)
    evaluator = CandidateEvaluator(create_executor(config),
        model if config.reward.policy == "dual" else None,
        PaperDualRewardPolicy(config.reward.test_weight, config.reward.llm_weight,
                              config.reward.critic_score_min, config.reward.critic_score_max))
    feedback = FeedbackService(mode=config.feedback.mode,
        trace_collector=DynamicTraceCollector(config.feedback.max_trace_visits,
            config.feedback.max_variables_per_frame, config.feedback.max_value_chars,
            backend=config.execution.backend, image=config.execution.image,
            max_container_items=config.feedback.max_container_items),
        block_analyzer=model, escalate_after=config.feedback.escalate_after,
        trace_timeout_seconds=config.feedback.trace_timeout_seconds,
        max_prompt_blocks=config.feedback.max_prompt_blocks,
        max_text_chars=config.feedback.max_feedback_tokens * 4)
    limits = BudgetLimits(**config.budget.model_dump())
    store = FileSystemRunStore(run_dir)
    kind = solver_type.lower()
    if kind == "mcts":
        solver = SearchEngine(model, model, model, evaluator, feedback,
            PUCBSelector(config.search.c_base, config.search.c),
            MeanBackupPolicy() if config.search.backup == "mean" else MaxBackupPolicy(),
            StoppingPolicy(config.search.max_depth, config.search.early_stop),
            FinalSelectionPolicy(config.search.final_selection), limits,
            config.search.width, config.search.max_depth, config.search.max_rethinks_per_node)
    elif kind == "direct":
        solver = DirectBaseline(model, evaluator, limits)
    elif kind in ("best_of_n", "bon"):
        if n < 1:
            raise ValueError("Best-of-N requires n >= 1")
        solver = BestOfNPublicBaseline(model, evaluator, limits, n)
    elif kind == "iterative_repair":
        solver = IterativeRepairBaseline(model, evaluator, limits, feedback)
    elif kind == "graph":
        solver = GraphSolver(gateway, evaluator, limits, prompts_dir=prompts_dir,
                             sampling=config.sampling, seed=config.experiment.seed,
                             require_exact_token_count=config.model.require_exact_token_count)
    else:
        raise ValueError(f"Unknown solver: {solver_type}")
    return solver, store


def create_search_engine(config, run_dir="runs/default"):
    return create_solver(config, "mcts", run_dir)
