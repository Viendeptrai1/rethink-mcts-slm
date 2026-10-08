"""
Response parsers and validators for structured JSON, code, and critic scores (§9.5).
"""

import json
import re
from typing import List, Tuple
from rethink_mcts.domain.errors import InvalidModelOutputError, GenerationTruncatedError


def strip_single_code_fence(text: str) -> str:
    """Strips at most one outer Markdown code fence (e.g. ```json ... ```)."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        # First line is ``` or ```json
        if len(lines) >= 2 and lines[-1].strip() == "```":
            return "\n".join(lines[1:-1]).strip()
    return text


def parse_thoughts_json(raw_text: str) -> List[Tuple[str, float]]:
    """
    Parses structured JSON response for proposals:
    {"thoughts": [{"text": "...", "reasonableness": 0.7}, ...]}
    U14: Validates JSON strictly; does NOT use regex to take the first number in explanations.
    """
    cleaned = strip_single_code_fence(raw_text)

    # 1. Try standard JSON parsing
    data = None
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"(\[.*\]|\{.*\})", cleaned, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
            except json.JSONDecodeError:
                pass

    results: List[Tuple[str, float]] = []
    if data is not None:
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            if "thoughts" in data and isinstance(data["thoughts"], list):
                items = data["thoughts"]
            elif "actions" in data and isinstance(data["actions"], list):
                items = data["actions"]
            elif "thought" in data or "text" in data:
                items = [data]
            else:
                items = []
        else:
            items = []

        for item in items:
            if not isinstance(item, dict):
                continue
            text = str(item.get("thought", item.get("text", ""))).strip()
            score = item.get("reasonableness", item.get("score", item.get("probability")))
            if not text or score is None:
                continue
            try:
                score_val = float(score)
                if score_val == score_val and score_val >= 0:
                    results.append((text, score_val))
            except (ValueError, TypeError):
                continue

    # 2. Check for repeated keys in one dict or text if regex finds more pairs
    t_matches = re.findall(r'\"(?:thought|text)\"\s*:\s*\"([^\"]+)\"', cleaned)
    s_matches = re.findall(r'\"(?:reasonableness|score|probability)\"\s*:\s*([0-9.]+)', cleaned)
    if len(t_matches) == len(s_matches) and len(t_matches) > len(results):
        alt_results = []
        for t, s in zip(t_matches, s_matches):
            try:
                alt_results.append((t.strip(), float(s)))
            except (ValueError, TypeError):
                pass
        if len(alt_results) > len(results):
            results = alt_results

    if not results:
        raise InvalidModelOutputError(f"Could not parse valid thought proposals from: {raw_text[:200]}")

    return results


def extract_python_code(raw_text: str) -> str:
    """
    Extracts Python source code from model response (U15).
    - If wrapped in ```python ... ```, extracts inner code.
    - If multiple conflicting codeblocks exist, raises InvalidModelOutputError.
    - If raw code without fences, returns stripped code.
    """
    text = raw_text.strip()
    blocks = re.findall(r"```(?:python)?\s*\n(.*?)\n```", text, re.DOTALL)

    if len(blocks) == 1:
        return blocks[0].strip()
    elif len(blocks) > 1:
        # Multiple code blocks
        raise InvalidModelOutputError(f"Model output contains {len(blocks)} conflicting code blocks")

    # If no triple-backtick block, check if it starts with ```
    if text.startswith("```") and text.endswith("```"):
        return strip_single_code_fence(text)

    # If unclosed code fence (e.g. truncated generation)
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 2:
            return "\n".join(lines[1:]).strip()

    return text


def parse_critic_score(raw_text: str, score_min: float = 0.0, score_max: float = 1.0) -> float:
    """
    Parses critic evaluation score (float in [score_min, score_max]).
    """
    cleaned = strip_single_code_fence(raw_text).strip()

    # 1. Try JSON
    if cleaned.startswith("{") and cleaned.endswith("}"):
        try:
            data = json.loads(cleaned)
            if "score" in data:
                val = float(data["score"])
                return max(score_min, min(score_max, val))
            if "evaluation" in data:
                val = float(data["evaluation"])
                return max(score_min, min(score_max, val))
        except Exception:
            pass

    # 2. Try parsing single float directly
    try:
        val = float(cleaned)
        return max(score_min, min(score_max, val))
    except ValueError:
        pass

    # 3. Look for explicit score/evaluation field or trailing number
    match = re.search(r"(?:score\s*[:=]\s*|rating\s*[:=]\s*|evaluation\s*[:=]\s*)?(-?\d+(?:\.\d+)?)", cleaned, re.IGNORECASE)
    if match:
        try:
            val = float(match.group(1))
            return max(score_min, min(score_max, val))
        except ValueError:
            pass

    raise InvalidModelOutputError(f"Could not parse critic score from '{raw_text}'")
