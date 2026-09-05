"""
Typed domain and application exceptions for RethinkMCTS.
"""


class RethinkMCTSError(Exception):
    """Base exception for all RethinkMCTS errors."""
    pass


# --- Configuration & Initialization Errors ---

class ConfigurationError(RethinkMCTSError):
    """Raised when configuration is invalid or inconsistent."""
    pass


class UnsupportedCapabilityError(RethinkMCTSError):
    """Raised when an adapter or model does not support a required capability."""
    pass


# --- Model & Provider Errors ---

class ModelError(RethinkMCTSError):
    """Base exception for model/gateway errors."""
    pass


class ProviderUnavailableError(ModelError):
    """Raised when LLM endpoint is unreachable (connection refused, DNS fail, 502/503/504)."""
    pass


class AuthenticationError(ModelError):
    """Raised when HTTP 401/403 occurs."""
    pass


class ModelNotFoundError(ModelError):
    """Raised when specified model tag/name does not exist on endpoint."""
    pass


class RateLimitedError(ModelError):
    """Raised when HTTP 429 occurs and retries/budget are exhausted."""
    pass


class GenerationTruncatedError(ModelError):
    """Raised when generation was cut off due to length limit (finish_reason == length)."""
    pass


class InvalidModelOutputError(ModelError):
    """Raised when model response cannot be parsed or violates schema contract."""
    pass


class ContextOverflowError(ModelError):
    """Raised when required task context exceeds prompt context budget."""
    pass


# --- Budget & Search Errors ---

class BudgetExceededError(RethinkMCTSError):
    """Raised when computational budget (calls, tokens, code generations, wall time) is exceeded."""
    pass


class TreeExhaustedError(RethinkMCTSError):
    """Raised when no further valid nodes/proposals can be explored."""
    pass


class InvariantViolationError(RethinkMCTSError):
    """Raised when a mathematical, data contract or revision invariant is violated."""
    pass


# --- Execution & Sandbox Errors ---

class ExecutionError(RethinkMCTSError):
    """Base exception for code execution and sandbox failures."""
    pass


class NoTestsError(ExecutionError):
    """Raised when evaluation is requested on an empty test suite."""
    pass


class LeakageDetectedError(RethinkMCTSError):
    """Raised when a hidden test or private fixture leaks into public context."""
    pass
