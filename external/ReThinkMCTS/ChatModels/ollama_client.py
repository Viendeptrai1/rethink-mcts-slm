from __future__ import annotations

import os
from typing import Any

from .modal_client import GenerationResult


class OllamaClient:
    """OpenAI-compatible client for an Ollama server."""

    def __init__(self, env_path: str = ".env") -> None:
        from dotenv import load_dotenv
        from openai import OpenAI

        load_dotenv(dotenv_path=env_path)
        self.model = os.getenv("LLM_MODEL", "qwen2.5:7b")
        base_url = os.getenv("LLM_BASE_URL", "http://127.0.0.1:11434/v1")
        api_key = os.getenv("LLM_API_KEY", "ollama")
        timeout = float(os.getenv("LLM_TIMEOUT_SECONDS", "600"))
        self._client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
        )

    def generate(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        max_tokens: int | None,
        temperature: float,
        top_p: float,
        reasoning_effort: str | None = None,
    ) -> GenerationResult:
        selected_model = model or self.model
        request: dict[str, Any] = {
            "model": selected_model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": False,
        }
        if max_tokens is not None:
            request["max_tokens"] = max_tokens
        if reasoning_effort:
            request["extra_body"] = {"reasoning_effort": reasoning_effort}

        response = self._client.chat.completions.create(**request)
        choice = response.choices[0]
        usage = response.usage
        return GenerationResult(
            content=choice.message.content or "",
            model=response.model or selected_model,
            finish_reason=choice.finish_reason,
            usage={
                "prompt_tokens": getattr(usage, "prompt_tokens", None),
                "completion_tokens": getattr(usage, "completion_tokens", None),
                "total_tokens": getattr(usage, "total_tokens", None),
            },
        )
