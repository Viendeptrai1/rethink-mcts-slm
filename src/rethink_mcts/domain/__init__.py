"""
RethinkMCTS Domain layer: core entities, contracts, and invariants.
"""

from rethink_mcts.domain.errors import (
    RethinkMCTSError,
    ConfigurationError,
    UnsupportedCapabilityError,
    ModelError,
    ProviderUnavailableError,
    AuthenticationError,
    ModelNotFoundError,
    RateLimitedError,
    GenerationTruncatedError,
    InvalidModelOutputError,
    ContextOverflowError,
    BudgetExceededError,
    TreeExhaustedError,
    InvariantViolationError,
    ExecutionError,
    NoTestsError,
    LeakageDetectedError,
)

from rethink_mcts.domain.problem import (
    ExecutionMode,
    StdinCase,
    FunctionCase,
    AssertionSuite,
    TestCase,
    ExecutionSpec,
    ProblemLimits,
    PublicMetadata,
    PublicProblem,
    HiddenSuite,
    JudgeSpec,
    HiddenProblem,
)

from rethink_mcts.domain.candidate import (
    CandidateVerdict,
    SingleCaseResult,
    ExecutionSummary,
    CandidateOrigin,
    ProgramCandidate,
    SelfEvalStatus,
    EvaluationRecord,
)

from rethink_mcts.domain.tree import (
    NodeStatus,
    CloseReason,
    ThoughtProposal,
    ProposalBatch,
    ThoughtRevision,
    SearchNode,
    Tree,
)

from rethink_mcts.domain.feedback import (
    ExecutionFacts,
    BlockVisit,
    TraceResult,
    BlockVerdict,
    BlockAssessment,
    BlockAnalysis,
    VerbalFeedback,
)

from rethink_mcts.domain.budget import (
    BudgetLimits,
    Usage,
    BudgetManager,
)

from rethink_mcts.domain.events import (
    EventEnvelope,
)
