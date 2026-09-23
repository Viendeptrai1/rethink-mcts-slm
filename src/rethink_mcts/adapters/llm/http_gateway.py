"""
OpenAI-compatible HTTP Model Gateway (§9.1, §9.3).
Handles URL normalization, retries, timeouts, and error mappings.
"""

import time
import json
import logging
from rethink_mcts.domain.errors import BudgetExceededError
from typing import Optional
import requests

from rethink_mcts.domain.errors import (
    ProviderUnavailableError,
    AuthenticationError,
    ModelNotFoundError,
    RateLimitedError,
    GenerationTruncatedError,
    ModelError
)
from rethink_mcts.ports.models import GenerationRequest, GenerationResponse, ModelGateway

logger = logging.getLogger(__name__)


def normalize_base_url(raw_url: str) -> str:
    """
    Normalizes OpenAI-compatible base URL (U16):
    - Strips whitespace and trailing slashes.
    - Strips trailing '/chat/completions' if user provided full endpoint URL.
    - Preserves existing path prefixes (e.g. '/proxy/llm/v1').
    """
    url = raw_url.strip().rstrip("/")
    if url.endswith("/chat/completions"):
        url = url[:-len("/chat/completions")].rstrip("/")
    return url


class HttpModelGateway(ModelGateway):
    """
    Gateway communicating with OpenAI-compatible HTTP endpoints (Ollama, vLLM, Modal, OpenAI).
    """
    def __init__(
        self,
        base_url: str,
        model_name: str,
        api_key: Optional[str] = None,
        timeout_seconds: float = 120.0,
        max_retries: int = 2
    ):
        self.base_url = normalize_base_url(base_url)
        self.model_name = model_name
        self.api_key = api_key or "ollama"
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.endpoint = f"{self.base_url}/chat/completions"

    def complete(self, request: GenerationRequest) -> GenerationResponse:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": request.prompt}
            ],
            "temperature": request.temperature,
            "top_p": request.top_p,
            "max_tokens": request.max_output_tokens
        }

        if request.seed is not None:
            payload["seed"] = request.seed

        if request.stop_sequences:
            payload["stop"] = list(request.stop_sequences)

        if request.response_contract == "json":
            payload["response_format"] = {"type": "json_object"}

        last_err: Optional[Exception] = None
        start_time = time.time()
        transport_attempts = 0

        for attempt in range(self.max_retries + 1):
            try:
                timeout = self.timeout_seconds
                if request.deadline is not None:
                    timeout = min(timeout, request.deadline - time.monotonic())
                    if timeout <= 0:
                        raise BudgetExceededError("Request deadline exhausted")
                transport_attempts += 1
                resp = requests.post(
                    self.endpoint,
                    headers=headers,
                    json=payload,
                    timeout=timeout
                )

                if resp.status_code == 200:
                    data = resp.json()
                    choice = data["choices"][0]
                    content = choice["message"]["content"] or ""
                    finish_reason = choice.get("finish_reason", "stop")

                    usage_data = data.get("usage", {})
                    p_tokens = usage_data.get("prompt_tokens")
                    c_tokens = usage_data.get("completion_tokens")

                    elapsed = time.time() - start_time
                    return GenerationResponse(
                        content=content,
                        finish_reason=finish_reason,
                        provider_request_id=data.get("id"),
                        model_id=data.get("model", self.model_name),
                        prompt_tokens=p_tokens,
                        completion_tokens=c_tokens,
                        transport_attempts=attempt + 1,
                        elapsed_seconds=elapsed
                    )

                # Error status handling (§9.3)
                if resp.status_code in (401, 403):
                    raise AuthenticationError(f"HTTP {resp.status_code} Authentication failed: {resp.text}")
                elif resp.status_code == 404:
                    raise ModelNotFoundError(f"HTTP 404 Model '{self.model_name}' or endpoint not found: {resp.text}")
                elif resp.status_code == 429:
                    # Rate limit retry with backoff
                    retry_after = 2 ** attempt
                    if "Retry-After" in resp.headers:
                        try:
                            retry_after = float(resp.headers["Retry-After"])
                        except ValueError:
                            pass
                    if attempt < self.max_retries:
                        time.sleep(min(retry_after, 10.0))
                        continue
                    raise RateLimitedError(f"HTTP 429 Rate limited after {self.max_retries} retries: {resp.text}")
                elif resp.status_code in (502, 503, 504):
                    if attempt < self.max_retries:
                        time.sleep(1.0 * (attempt + 1))
                        continue
                    raise ProviderUnavailableError(f"HTTP {resp.status_code} Provider unavailable: {resp.text}")
                else:
                    raise ModelError(f"HTTP {resp.status_code} Unexpected provider error: {resp.text}")

            except (requests.ConnectionError, requests.Timeout) as e:
                last_err = e
                if attempt < self.max_retries:
                    time.sleep(1.0 * (attempt + 1))
                    continue
                error = ProviderUnavailableError(f"Connection failed to endpoint '{self.endpoint}': {e}")
                error.transport_attempts = attempt + 1
                raise error from e
            except Exception as exc:
                # Include HTTP errors and malformed provider responses after retries.
                exc.transport_attempts = transport_attempts
                raise

        raise ProviderUnavailableError(f"Request failed after {self.max_retries} attempts: {last_err}")
