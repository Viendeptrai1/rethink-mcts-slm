"""Private Modal Function serving pinned generator and optional evaluator models."""

from __future__ import annotations

import json
import os
import subprocess
import time
from urllib.request import Request, urlopen

import modal


APP_NAME = "rethinkmcts-qwen25-ollama"
MODEL = "qwen2.5-coder:7b-instruct"
EVALUATOR_MODEL = "qwen2.5-coder:14b-instruct"
ALLOWED_MODELS = {MODEL, EVALUATOR_MODEL}
OLLAMA_URL = "http://127.0.0.1:11434"

app = modal.App(APP_NAME)
model_volume = modal.Volume.from_name("rethinkmcts-ollama-models", create_if_missing=True)
image = modal.Image.from_registry(
    "ollama/ollama:0.35.1",
    add_python="3.11",
    setup_dockerfile_commands=["ENTRYPOINT []"],
)


def _request(path: str, payload: dict | None = None, *, timeout: float = 30) -> dict:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        f"{OLLAMA_URL}{path}",
        data=body,
        headers={"Content-Type": "application/json"} if body is not None else {},
    )
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


@app.cls(
    image=image,
    gpu="L40S",
    volumes={"/root/.ollama": model_volume},
    max_containers=4,
    scaledown_window=120,
    timeout=1200,
    startup_timeout=1200,
)
class OllamaInference:
    def _ensure_model(self, model_name: str) -> dict:
        if model_name not in ALLOWED_MODELS:
            raise ValueError(f"Model is not allow-listed: {model_name}")
        entries = _request("/api/tags").get("models", [])
        model = next((item for item in entries if item.get("name") == model_name), None)
        if model is None:
            subprocess.run(["ollama", "pull", model_name], check=True, timeout=900)
            model_volume.commit()
            entries = _request("/api/tags").get("models", [])
            model = next((item for item in entries if item.get("name") == model_name), None)
        if not model or not model.get("digest"):
            raise RuntimeError(f"Model {model_name} is absent after pull")
        return model

    @modal.enter()
    def start(self) -> None:
        os.environ["OLLAMA_HOST"] = "127.0.0.1:11434"
        self.server = subprocess.Popen(
            ["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        for _ in range(60):
            if self.server.poll() is not None:
                raise RuntimeError("Ollama server exited during startup")
            try:
                _request("/api/tags", timeout=2)
                break
            except OSError:
                time.sleep(1)
        else:
            raise TimeoutError("Ollama server did not become ready")
        self._ensure_model(MODEL)

    @modal.method()
    def model_info(self, include_evaluator: bool = False) -> dict:
        models = {MODEL: self._ensure_model(MODEL)}
        if include_evaluator:
            models[EVALUATOR_MODEL] = self._ensure_model(EVALUATOR_MODEL)
        gpu = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            check=True, capture_output=True, text=True, timeout=10,
        )
        version = subprocess.run(
            ["ollama", "--version"], check=True, capture_output=True, text=True, timeout=10,
        )
        return {
            "model": MODEL,
            "digest": models[MODEL]["digest"],
            "models": {name: {"digest": value["digest"]} for name, value in models.items()},
            "gpu": gpu.stdout.strip(),
            "ollama_version": (version.stdout or version.stderr).strip(),
        }

    @modal.method()
    def generate(
        self,
        messages: list[dict[str, str]],
        model: str,
        max_tokens: int | None,
        temperature: float,
        top_p: float,
    ) -> dict:
        self._ensure_model(model)
        options = {"temperature": temperature, "top_p": top_p}
        if max_tokens is not None:
            options["num_predict"] = max_tokens
        response = _request(
            "/api/chat",
            {"model": model, "messages": messages, "stream": False, "options": options},
            timeout=1100,
        )
        loaded = _request("/api/ps").get("models", [])
        if not any(
            item.get("name") == model and int(item.get("size_vram") or 0) > 0
            for item in loaded
        ):
            raise RuntimeError("Ollama did not report the model loaded in GPU VRAM")
        return {
            "content": response.get("message", {}).get("content", ""),
            "model": response.get("model", model),
            "finish_reason": response.get("done_reason"),
            "usage": {
                "prompt_tokens": response.get("prompt_eval_count"),
                "completion_tokens": response.get("eval_count"),
                "total_tokens": (response.get("prompt_eval_count") or 0) + (response.get("eval_count") or 0),
            },
        }
