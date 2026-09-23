"""One accounting boundary for semantic calls and gateway requests."""
from dataclasses import asdict, replace
import time
from rethink_mcts.domain.errors import GenerationTruncatedError, ModelError


def invoke_model(budget, model, method, role, **kwargs):
    if getattr(model, "meters_requests", False):
        previous = model.budget
        model.budget = budget
        try:
            return getattr(model, method)(**kwargs)
        finally:
            model.budget = previous
    budget.before_model_call(role)
    budget.usage.transport_attempts += 1
    # Semantic mocks have no measured tokens. Do not report zero consumption.
    return getattr(model, method)(**kwargs)


def complete_request(gateway, request, budget=None):
    if budget is None:
        return gateway.complete(request)
    budget.before_model_call(request.role)
    request = replace(request, deadline=time.monotonic() + budget.remaining_seconds())
    record = {"request": asdict(request), "response": None, "error": None}
    budget.requests.append(record)
    try:
        response = gateway.complete(request)
    except Exception as exc:
        budget.usage.transport_attempts += getattr(exc, "transport_attempts", 1)
        record["error"] = {"type": type(exc).__name__, "message": str(exc)}
        raise
    budget.usage.transport_attempts += response.transport_attempts
    budget.record_response(response, request.role)
    if response.transport_attempts > 1:
        # Usage of failed transport attempts is not reported by the provider.
        budget.usage.missing_token_calls += response.transport_attempts - 1
        budget.usage.tokens_by_role[request.role]["missing_calls"] += response.transport_attempts - 1
    record["response"] = asdict(response)
    if response.finish_reason == "length":
        raise GenerationTruncatedError("Provider truncated generation at the output limit")
    return response
