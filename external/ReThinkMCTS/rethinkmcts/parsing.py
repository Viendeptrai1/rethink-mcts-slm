from __future__ import annotations

import json
import math
import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ThoughtProposal(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    thought: str = Field(min_length=1)
    reasonableness: float = Field(ge=0.0, le=1.0, allow_inf_nan=False)


def _json_payload(text: str) -> Any:
    stripped = text.strip()
    fenced = re.findall(r"```(?:json)?\s*\n?(.*?)```", stripped, flags=re.DOTALL | re.IGNORECASE)
    candidates = fenced or [stripped]
    for candidate in candidates:
        try:
            return json.loads(candidate.strip())
        except json.JSONDecodeError:
            continue
    start = min((index for index in (stripped.find("["), stripped.find("{")) if index >= 0), default=-1)
    if start >= 0:
        for end in range(len(stripped), start, -1):
            try:
                return json.loads(stripped[start:end])
            except json.JSONDecodeError:
                continue
    raise ValueError("LLM response does not contain valid JSON")


def parse_thoughts(text: str, *, width: int = 3) -> list[ThoughtProposal]:
    if width <= 0:
        raise ValueError("width must be greater than zero")
    payload = _json_payload(text)
    if isinstance(payload, dict):
        payload = payload.get("thoughts", payload.get("actions", []))
    if not isinstance(payload, list):
        raise ValueError("thought expansion must be a JSON list")
    if len(payload) != width:
        raise ValueError(f"LLM expansion must contain exactly {width} thoughts")

    proposals: list[ThoughtProposal] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        thought = item.get("thought")
        if thought is None:
            thought = next((value for key, value in item.items() if str(key).lower().startswith("thought")), None)
        score = item.get("reasonableness", item.get("Reasonableness", item.get("probability", 0.0)))
        if not isinstance(thought, str) or not thought.strip():
            continue
        try:
            numeric_score = float(score)
        except (TypeError, ValueError):
            numeric_score = 0.0
        if not math.isfinite(numeric_score):
            raise ValueError("LLM expansion score must be finite")
        proposals.append(ThoughtProposal(thought=thought.strip(), reasonableness=max(0.0, min(1.0, numeric_score))))
    if len(proposals) != width:
        raise ValueError(f"LLM expansion must contain exactly {width} usable thoughts")
    if len({item.thought.casefold() for item in proposals}) != width:
        raise ValueError("LLM expansion thoughts must be distinct")
    total = sum(item.reasonableness for item in proposals)
    if total <= 0:
        uniform = 1.0 / len(proposals)
        return [ThoughtProposal(thought=item.thought, reasonableness=uniform) for item in proposals]
    return [
        ThoughtProposal(thought=item.thought, reasonableness=item.reasonableness / total)
        for item in proposals
    ]


def parse_score(text: str) -> float:
    payload: Any
    try:
        payload = _json_payload(text)
    except ValueError:
        payload = None
    value: Any = payload
    if isinstance(payload, dict):
        value = payload.get("evaluation", payload.get("score", payload.get("value")))
    if value is None:
        match = re.search(r"[-+]?\d+(?:\.\d+)?", text)
        if not match:
            raise ValueError("LLM response does not contain a numeric score")
        value = match.group(0)
    try:
        return max(-1.0, min(1.0, float(value)))
    except (TypeError, ValueError) as exc:
        raise ValueError("LLM score is not numeric") from exc


def extract_code(text: str) -> str:
    fenced = re.findall(r"```(?:python|py)?\s*\n?(.*?)```", text.strip(), flags=re.DOTALL | re.IGNORECASE)
    return max(fenced, key=len).strip() if fenced else text.strip()


def parse_feedback(text: str) -> dict[str, Any]:
    try:
        payload = _json_payload(text)
    except ValueError:
        return {"raw": text.strip()}
    return payload if isinstance(payload, dict) else {"raw": text.strip(), "parsed": payload}
