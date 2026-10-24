from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from DataProcess import Problem


SYSTEM_PROMPTS = {
    "v1": """You are an expert Python programmer.
Solve the given programming problem correctly and efficiently.
Return only complete Python source code. Do not use Markdown fences and do not explain the solution."""
}


@dataclass(frozen=True)
class DirectGenerationConfig:
    run_name: str
    model: str | None
    prompt_version: str
    max_tokens: int | None
    temperature: float
    top_p: float
    reasoning_effort: str | None

    @property
    def system_prompt(self) -> str:
        return SYSTEM_PROMPTS[self.prompt_version]

    def validate(self) -> None:
        if not self.run_name.strip():
            raise ValueError("run_name must not be empty")
        if self.prompt_version not in SYSTEM_PROMPTS:
            available = ", ".join(sorted(SYSTEM_PROMPTS))
            raise ValueError(f"Unknown prompt_version. Available: {available}")
        if self.max_tokens is not None and self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        if not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be between 0 and 2")
        if not 0 < self.top_p <= 1:
            raise ValueError("top_p must be in (0, 1]")


def load_config(path: str | Path) -> DirectGenerationConfig:
    config_path = Path(path)
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    generation = payload["generation"]
    config = DirectGenerationConfig(
        run_name=payload["run_name"],
        model=payload.get("model"),
        prompt_version=payload["prompt_version"],
        max_tokens=generation["max_tokens"],
        temperature=generation["temperature"],
        top_p=generation["top_p"],
        reasoning_effort=generation.get("reasoning_effort"),
    )
    config.validate()
    return config


def build_user_prompt(problem: Problem) -> str:
    if problem.dataset == "apps":
        parts = ["Programming problem:\n", problem.statement.strip()]
        if problem.starter_code.strip():
            parts.extend(
                [
                    "\n\nStarter code:\n",
                    problem.starter_code.rstrip(),
                    "\n\nComplete the starter code and return the full program.",
                ]
            )
        else:
            parts.append("\n\nReturn a complete program that reads input and writes output.")
        return "".join(parts)

    return (
        "Complete the following Python function. Return the full Python source, "
        "including the supplied signature and docstring.\n\n"
        f"{problem.statement.rstrip()}"
    )


def extract_code(response: str) -> str:
    text = response.strip()
    fenced = re.findall(r"```(?:python|py)?\s*\n?(.*?)```", text, flags=re.DOTALL | re.I)
    if fenced:
        return max(fenced, key=len).strip()
    return text


def is_complete_artifact(
    metadata: dict[str, object],
    solution_path: Path,
    response_path: Path | None = None,
) -> bool:
    if response_path is not None:
        try:
            if not response_path.is_file() or not response_path.read_text(encoding="utf-8").strip():
                return False
        except OSError:
            return False
    if not solution_path.is_file():
        return False
    try:
        if not solution_path.read_text(encoding="utf-8").strip():
            return False
    except OSError:
        return False
    if metadata.get("generation_complete") is False:
        return False
    finish_reason = metadata.get("finish_reason")
    return finish_reason in (None, "stop")


def safe_path_component(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._")
    return cleaned or "unnamed"


def save_artifact(
    output_root: Path,
    *,
    run_name: str,
    model: str,
    problem: Problem,
    user_prompt: str,
    raw_response: str,
    code: str,
    metadata: dict[str, object],
) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    run_dir = (
        output_root
        / "direct_generation"
        / safe_path_component(run_name)
        / safe_path_component(model)
        / problem.dataset
        / f"{safe_path_component(problem.problem_id)}_{timestamp}"
    )
    run_dir.mkdir(parents=True, exist_ok=False)

    (run_dir / "problem.txt").write_text(user_prompt, encoding="utf-8")
    (run_dir / "response.txt").write_text(raw_response, encoding="utf-8")
    (run_dir / "solution.py").write_text(code + "\n", encoding="utf-8")
    (run_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return run_dir
