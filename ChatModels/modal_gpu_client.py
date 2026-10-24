"""Authenticated Modal Function client; no public inference URL or proxy secret."""

from __future__ import annotations

import os

from .modal_client import GenerationResult


APP_NAME = "rethinkmcts-qwen25-ollama"
CLASS_NAME = "OllamaInference"


class ModalGpuClient:
    def __init__(self, env_path: str = ".env") -> None:
        from dotenv import load_dotenv
        import modal

        load_dotenv(dotenv_path=env_path)
        self.model = os.getenv("LLM_MODEL", "qwen2.5-coder:7b-instruct")
        self._instance = modal.Cls.from_name(APP_NAME, CLASS_NAME)()

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
        if reasoning_effort is not None:
            raise ValueError("Modal Ollama adapter does not support reasoning_effort")
        result = self._instance.generate.remote(
            messages, model or self.model, max_tokens, temperature, top_p
        )
        return GenerationResult(**result)
