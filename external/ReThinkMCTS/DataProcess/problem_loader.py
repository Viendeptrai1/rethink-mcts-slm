from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_ROOT = PROJECT_ROOT / "data"


@dataclass(frozen=True)
class Problem:
    dataset: str
    problem_id: str
    statement: str
    starter_code: str = ""
    entry_point: str | None = None


def _load_apps(problem_id: str, split: str, data_root: Path) -> Problem:
    try:
        numeric_id = int(problem_id)
    except ValueError as exc:
        raise ValueError("APPS problem_id must be an integer from 0 to 4999") from exc

    if numeric_id < 0 or numeric_id > 4999:
        raise ValueError("APPS problem_id must be between 0 and 4999")
    if split not in {"train", "test"}:
        raise ValueError("APPS split must be 'train' or 'test'")

    problem_dir = data_root / "apps" / "raw" / split / f"{numeric_id:04d}"
    question_path = problem_dir / "question.txt"
    if not question_path.is_file():
        raise FileNotFoundError(f"APPS problem not found: {question_path}")

    starter_path = problem_dir / "starter_code.py"
    starter_code = (
        starter_path.read_text(encoding="utf-8") if starter_path.is_file() else ""
    )
    return Problem(
        dataset="apps",
        problem_id=f"{numeric_id:04d}",
        statement=question_path.read_text(encoding="utf-8"),
        starter_code=starter_code,
    )


def _load_humaneval(problem_id: str, data_root: Path) -> Problem:
    try:
        numeric_id = int(problem_id.removeprefix("HumanEval/"))
    except ValueError as exc:
        raise ValueError(
            "HumanEval problem_id must be an integer or have form HumanEval/<id>"
        ) from exc

    if numeric_id < 0 or numeric_id > 163:
        raise ValueError("HumanEval problem_id must be between 0 and 163")

    from datasets import load_from_disk

    dataset_path = data_root / "humaneval" / "arrow"
    if not dataset_path.is_dir():
        raise FileNotFoundError(f"HumanEval dataset not found: {dataset_path}")

    row = load_from_disk(str(dataset_path))["test"][numeric_id]
    return Problem(
        dataset="humaneval",
        problem_id=row["task_id"],
        statement=row["prompt"],
        entry_point=row["entry_point"],
    )


def load_problem(
    dataset: str,
    problem_id: str,
    *,
    split: str = "test",
    data_root: str | Path = DEFAULT_DATA_ROOT,
) -> Problem:
    normalized = dataset.lower()
    root = Path(data_root)
    if normalized == "apps":
        return _load_apps(problem_id, split, root)
    if normalized == "humaneval":
        return _load_humaneval(problem_id, root)
    raise ValueError("dataset must be 'apps' or 'humaneval'")
