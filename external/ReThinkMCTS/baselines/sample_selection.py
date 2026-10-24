from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_problem_ids(path: str | Path, *, dataset: str) -> list[int]:
    """Load and validate an immutable benchmark sample manifest."""
    sample_path = Path(path).resolve()
    payload = json.loads(sample_path.read_text(encoding="utf-8"))
    if payload.get("dataset") != dataset:
        raise ValueError(
            f"Sample manifest {sample_path} is for {payload.get('dataset')!r}, "
            f"not {dataset!r}."
        )
    if payload.get("split", "test") != "test":
        raise ValueError(f"Only the test split is supported by benchmark samples: {sample_path}")
    problem_ids = payload.get("problem_ids")
    if not isinstance(problem_ids, list) or not problem_ids:
        raise ValueError(f"Sample manifest has no problem_ids: {sample_path}")
    if not all(isinstance(problem_id, int) and not isinstance(problem_id, bool) for problem_id in problem_ids):
        raise ValueError(f"Sample manifest problem_ids must be integers: {sample_path}")
    if len(set(problem_ids)) != len(problem_ids):
        raise ValueError(f"Sample manifest contains duplicate problem IDs: {sample_path}")
    maximum_id = 4999 if dataset == "apps" else 163
    invalid = [problem_id for problem_id in problem_ids if not 0 <= problem_id <= maximum_id]
    if invalid:
        raise ValueError(
            f"Sample manifest contains out-of-range IDs for {dataset}: {invalid[:5]}"
        )
    declared_size = payload.get("sample_size")
    if declared_size is not None and declared_size != len(problem_ids):
        raise ValueError(
            f"sample_size={declared_size} does not match {len(problem_ids)} IDs: {sample_path}"
        )
    return problem_ids


def problem_keys(path: str | Path, *, dataset: str) -> set[str]:
    problem_ids = load_problem_ids(path, dataset=dataset)
    if dataset == "apps":
        return {f"{problem_id:04d}" for problem_id in problem_ids}
    return {f"HumanEval/{problem_id}" for problem_id in problem_ids}


def load_sample_manifest(path: str | Path, *, dataset: str) -> dict[str, Any]:
    """Load a validated sample manifest, including optional APPS metadata."""
    sample_path = Path(path).resolve()
    payload = json.loads(sample_path.read_text(encoding="utf-8"))
    load_problem_ids(sample_path, dataset=dataset)
    if payload.get("sample_id") is None:
        raise ValueError(f"Sample manifest is missing sample_id: {sample_path}")
    if payload.get("seed") is None:
        raise ValueError(f"Sample manifest is missing seed: {sample_path}")
    if dataset == "apps":
        difficulty_map = payload.get("difficulty_by_problem_id")
        if not isinstance(difficulty_map, dict):
            raise ValueError(
                "APPS evaluation manifest must contain difficulty_by_problem_id: "
                f"{sample_path}"
            )
        expected = {str(problem_id) for problem_id in payload["problem_ids"]}
        if set(difficulty_map) != expected:
            raise ValueError(
                "difficulty_by_problem_id must contain exactly all APPS problem IDs: "
                f"{sample_path}"
            )
    payload["manifest_path"] = str(sample_path)
    return payload
