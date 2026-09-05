"""
Pydantic v2 strict configuration schema matching §12 of RethinkMCTS specification.
"""

from typing import Any, List, Optional
import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator
from rethink_mcts.domain.errors import ConfigurationError


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ModelConfig(StrictBaseModel):
    transport: str = "openai_compatible"
    base_url: str = "http://localhost:11434/v1"
    model: str = "qwen2.5-coder:7b-instruct"
    api_key_env: Optional[str] = None
    request_timeout_seconds: float = 120.0
    max_transport_retries: int = 2
    max_format_retries: int = 1
    concurrency: int = 1
    context_window_tokens: int = 8192
    context_safety_margin_tokens: int = 256
    structured_output: str = "auto"
    require_exact_token_count: bool = False


class PromptConfig(StrictBaseModel):
    bundle: str = "compact_v1"
    language: str = "en"


class SamplingRoleConfig(StrictBaseModel):
    temperature: float = 0.0
    top_p: float = 0.95
    max_output_tokens: int = 512


class SamplingConfig(StrictBaseModel):
    expansion: SamplingRoleConfig = Field(default_factory=lambda: SamplingRoleConfig(temperature=0.6, top_p=0.95, max_output_tokens=384))
    code: SamplingRoleConfig = Field(default_factory=lambda: SamplingRoleConfig(temperature=0.2, top_p=0.95, max_output_tokens=1536))
    rethink: SamplingRoleConfig = Field(default_factory=lambda: SamplingRoleConfig(temperature=0.3, top_p=0.95, max_output_tokens=192))
    critic: SamplingRoleConfig = Field(default_factory=lambda: SamplingRoleConfig(temperature=0.0, top_p=1.0, max_output_tokens=160))
    block_analysis: SamplingRoleConfig = Field(default_factory=lambda: SamplingRoleConfig(temperature=0.0, top_p=1.0, max_output_tokens=768))


class SearchConfig(StrictBaseModel):
    algorithm: str = "rethink_mcts"
    width: int = 3
    max_depth: int = 4
    max_rethinks_per_node: int = 1
    selection: str = "p_ucb"
    c_base: float = 10.0
    c: float = 4.0
    prior: str = "llm_reasonableness"
    prior_fallback: str = "uniform_after_retry"
    backup: str = "max"
    leaf_revision_policy: str = "reset_leaf_keep_ancestor_history"
    early_stop: str = "none"
    final_selection: str = "max_reward"


class RewardConfig(StrictBaseModel):
    policy: str = "dual"
    test_weight: float = 0.8
    llm_weight: float = 0.2
    critic_score_min: float = 0.0
    critic_score_max: float = 1.0
    invalid_critic_policy: str = "zero_after_retry"


class FeedbackConfig(StrictBaseModel):
    mode: str = "block"  # "block" | "facts_only" | "none"
    max_failed_tests: int = 1
    max_feedback_tokens: int = 1536
    max_trace_visits: int = 256
    max_prompt_blocks: int = 32
    max_variables_per_frame: int = 20
    max_value_chars: int = 160
    max_snapshot_depth: int = 2
    max_container_items: int = 10
    trace_timeout_seconds: float = 5.0
    on_trace_failure: str = "execution_facts"


class BudgetConfig(StrictBaseModel):
    max_code_generations: int = 8
    max_search_iterations: int = 64
    max_model_calls: int = 64
    max_total_tokens: int = 65536
    max_wall_seconds: float = 900.0
    max_sandbox_runs: int = 1000


class ExecutionConfig(StrictBaseModel):
    backend: str = "trusted_fixture"  # "trusted_fixture" | "docker"
    image: str = "rethink-worker:py311"
    require_pinned_digest_for_benchmark: bool = False
    per_test_timeout_seconds: float = 2.0
    memory_mb: int = 512
    pids_limit: int = 32
    cpus: float = 1.0
    stdout_limit_bytes: int = 1048576
    stderr_limit_bytes: int = 262144
    network: str = "none"
    python_time_multiplier: float = 2.5


class DataConfig(StrictBaseModel):
    adapter: str = "synthetic"
    prepared_public_path: Optional[str] = None
    split: str = "validation"
    require_python3_solution: bool = True
    min_rating: Optional[int] = None
    max_rating: Optional[int] = None
    missing_public_policy: str = "exclude"


class StorageConfig(StrictBaseModel):
    output_dir: str = "runs"
    save_raw_model_responses: bool = True
    save_trace: bool = True
    execution_cache: bool = True
    generation_cache_mode: str = "off"
    checkpoint: str = "after_evaluation_transaction"

    @model_validator(mode="before")
    @classmethod
    def normalize_cache_mode(cls, data: Any) -> Any:
        if isinstance(data, dict):
            val = data.get("generation_cache_mode")
            if val is False:
                data["generation_cache_mode"] = "off"
            elif val is True:
                data["generation_cache_mode"] = "on"
        return data


class ExperimentConfig(StrictBaseModel):
    seed: int = 42
    role_models: str = "same_as_generator"
    allow_mock: bool = False
    deviations: List[str] = Field(default_factory=list)


class AppConfig(StrictBaseModel):
    schema_version: int = 1
    profile: str = "small_model"
    algorithm_spec_version: str = "1.0"

    model: ModelConfig = Field(default_factory=ModelConfig)
    prompts: PromptConfig = Field(default_factory=PromptConfig)
    sampling: SamplingConfig = Field(default_factory=SamplingConfig)
    search: SearchConfig = Field(default_factory=SearchConfig)
    reward: RewardConfig = Field(default_factory=RewardConfig)
    feedback: FeedbackConfig = Field(default_factory=FeedbackConfig)
    budget: BudgetConfig = Field(default_factory=BudgetConfig)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    experiment: ExperimentConfig = Field(default_factory=ExperimentConfig)

    @model_validator(mode="after")
    def validate_cross_field_rules(self) -> "AppConfig":
        # Validate critic range consistency
        if self.reward.critic_score_min >= self.reward.critic_score_max:
            raise ConfigurationError(
                f"critic_score_min ({self.reward.critic_score_min}) must be strictly less than critic_score_max ({self.reward.critic_score_max})"
            )
        # Validate budget non-negativity
        if self.budget.max_code_generations <= 0:
            raise ConfigurationError("budget.max_code_generations must be positive")
        if self.search.width <= 0:
            raise ConfigurationError("search.width must be positive")
        return self

    @classmethod
    def from_yaml_file(cls, path: str) -> "AppConfig":
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f)
            if not isinstance(raw, dict):
                raise ConfigurationError(f"Config file at '{path}' must be a YAML dictionary")
            return cls(**raw)
        except Exception as e:
            if isinstance(e, ConfigurationError):
                raise
            raise ConfigurationError(f"Failed to load configuration from '{path}': {e}") from e
