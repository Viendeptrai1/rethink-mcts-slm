"""
Model ports and protocol contracts.
"""

from dataclasses import dataclass, field
from typing import Optional, Protocol, runtime_checkable
from rethink_mcts.domain.problem import ExecutionSpec
from rethink_mcts.domain.tree import ProposalBatch
from rethink_mcts.domain.feedback import ExecutionFacts, TraceResult, BlockAnalysis, VerbalFeedback


@dataclass(frozen=True)
class GenerationRequest:
    request_id: str
    role: str  # "expansion" | "code" | "rethink" | "critic" | "block_analysis"
    prompt: str
    temperature: float = 0.0
    top_p: float = 1.0
    max_output_tokens: int = 1024
    response_contract: str = "text"  # "text" | "json"
    stop_sequences: tuple[str, ...] = ()
    seed: Optional[int] = None
    deadline: Optional[float] = None


@dataclass(frozen=True)
class GenerationResponse:
    content: str
    finish_reason: str
    provider_request_id: Optional[str] = None
    model_id: Optional[str] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    elapsed_seconds: float = 0.0
    raw_response_ref: Optional[str] = None
    transport_attempts: int = 1


@runtime_checkable
class ModelGateway(Protocol):
    """Low-level protocol communicating with LLM endpoints."""
    def complete(self, request: GenerationRequest) -> GenerationResponse:
        ...


@runtime_checkable
class ThoughtProposer(Protocol):
    """Proposes k next reasoning steps with reasonableness scores."""
    def propose(
        self,
        statement: str,
        active_thoughts: tuple[str, ...],
        width: int,
        feedback: Optional[VerbalFeedback] = None
    ) -> ProposalBatch:
        ...


@runtime_checkable
class CodeGenerator(Protocol):
    """Generates complete runnable program from active thoughts and task specification."""
    def generate(
        self,
        statement: str,
        execution_spec: ExecutionSpec,
        active_thoughts: tuple[str, ...],
        public_examples_str: str = ""
    ) -> str:
        ...


@runtime_checkable
class ThoughtRefiner(Protocol):
    """Refines an erroneous thought based on verbal feedback."""
    def refine(
        self,
        statement: str,
        execution_spec: ExecutionSpec,
        parent_thoughts: tuple[str, ...],
        erroneous_thought: str,
        candidate_code: str,
        feedback: VerbalFeedback
    ) -> str:
        ...


@runtime_checkable
class CodeCritic(Protocol):
    """Self-evaluates code correctness and robustness when public tests pass."""
    def assess(
        self,
        statement: str,
        candidate_code: str
    ) -> float:
        ...


@runtime_checkable
class BlockAnalyzer(Protocol):
    """Analyzes dynamic bytecode trace blocks to identify fault locations."""
    def analyze(
        self,
        statement: str,
        candidate_code: str,
        facts: ExecutionFacts,
        trace: TraceResult
    ) -> BlockAnalysis:
        ...
