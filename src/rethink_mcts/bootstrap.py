"""
Bootstrap dependency injection factory (§3.1, §3.2).
Single entry point connecting configuration with ports and concrete adapters.
"""

import os
from rethink_mcts.config import AppConfig
from rethink_mcts.domain.budget import BudgetLimits
from rethink_mcts.policies.selection import PUCBSelector
from rethink_mcts.policies.prior import PriorPolicy
from rethink_mcts.policies.backup import MaxBackupPolicy
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


def create_search_engine(config: AppConfig, run_dir: str = "runs/default") -> tuple[SearchEngine, FileSystemRunStore]:
    """
    Creates and wires all ports and adapters based on AppConfig.
    """
    # 1. Model Gateway & Semantic Ports
    if config.model.transport == "mock" or config.experiment.allow_mock:
        model_adapter = ScenarioMockLLM()
    else:
        api_key = os.environ.get(config.model.api_key_env, "ollama") if config.model.api_key_env else "ollama"
        gateway = HttpModelGateway(
            base_url=config.model.base_url,
            model_name=config.model.model,
            api_key=api_key,
            timeout_seconds=config.model.request_timeout_seconds,
            max_retries=config.model.max_transport_retries
        )
        prior_policy = PriorPolicy(fallback_mode=config.search.prior_fallback)
        prompts_dir = f"prompts/{config.prompts.bundle}"
        model_adapter = SemanticPromptedLLM(
            gateway=gateway,
            prompts_dir=prompts_dir,
            prior_policy=prior_policy
        )

    # 2. Execution Backend
    if config.execution.backend == "docker":
        executor = DockerExecutor(image=config.execution.image, allow_host_fallback=True)
    else:
        executor = TrustedFixtureExecutor()

    # 3. Tracing & Feedback
    if config.feedback.mode == "block":
        trace_collector = DynamicTraceCollector(
            max_visits=config.feedback.max_trace_visits,
            max_variables_per_frame=config.feedback.max_variables_per_frame,
            max_value_chars=config.feedback.max_value_chars
        )
        block_analyzer = model_adapter
    else:
        trace_collector = None
        block_analyzer = None

    feedback_service = FeedbackService(
        mode=config.feedback.mode,
        trace_collector=trace_collector,
        block_analyzer=block_analyzer
    )

    # 4. Reward & Evaluation
    reward_policy = PaperDualRewardPolicy(
        test_weight=config.reward.test_weight,
        llm_weight=config.reward.llm_weight,
        critic_min=config.reward.critic_score_min,
        critic_max=config.reward.critic_score_max
    )
    evaluator = CandidateEvaluator(
        executor=executor,
        critic=model_adapter,
        reward_policy=reward_policy
    )

    # 5. Policies
    selector = PUCBSelector(c_base=config.search.c_base, c=config.search.c)
    backup_policy = MaxBackupPolicy()
    stopping_policy = StoppingPolicy(max_depth=config.search.max_depth, early_stop_mode=config.search.early_stop)
    final_selector = FinalSelectionPolicy(mode=config.search.final_selection)

    budget_limits = BudgetLimits(
        max_code_generations=config.budget.max_code_generations,
        max_search_iterations=config.budget.max_search_iterations,
        max_model_calls=config.budget.max_model_calls,
        max_total_tokens=config.budget.max_total_tokens,
        max_wall_seconds=config.budget.max_wall_seconds,
        max_sandbox_runs=config.budget.max_sandbox_runs
    )

    # 6. Storage
    store = FileSystemRunStore(run_dir=run_dir)

    # 7. Search Engine
    engine = SearchEngine(
        proposer=model_adapter,
        generator=model_adapter,
        refiner=model_adapter,
        evaluator=evaluator,
        feedback_service=feedback_service,
        selector=selector,
        backup_policy=backup_policy,
        stopping_policy=stopping_policy,
        final_selector=final_selector,
        budget_limits=budget_limits,
        width=config.search.width,
        max_depth=config.search.max_depth,
        max_rethinks_per_node=config.search.max_rethinks_per_node
    )

    return engine, store
