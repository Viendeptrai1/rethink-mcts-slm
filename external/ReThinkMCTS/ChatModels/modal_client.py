from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_ENV_VARS = (
    "MODAL_PROXY_TOKEN_ID",
    "MODAL_PROXY_TOKEN_SECRET",
    "MODAL_BASE_URL",
    "KIMI_MODEL",
)


@dataclass(frozen=True)
class GenerationResult:
    content: str
    model: str
    finish_reason: str | None
    usage: dict[str, int | None]


class ModalClient:
    def __init__(self, env_path: str | Path = ".env") -> None:
        from dotenv import load_dotenv
        from openai import OpenAI

        load_dotenv(dotenv_path=env_path)
        missing = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
        if missing:
            names = ", ".join(missing)
            raise RuntimeError(f"Missing required environment variables: {names}")

        self.model = os.environ["KIMI_MODEL"]
        token = (
            f"{os.environ['MODAL_PROXY_TOKEN_ID']}."
            f"{os.environ['MODAL_PROXY_TOKEN_SECRET']}"
        )
        self._client = OpenAI(
            base_url=os.environ["MODAL_BASE_URL"],
            api_key=token,
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
