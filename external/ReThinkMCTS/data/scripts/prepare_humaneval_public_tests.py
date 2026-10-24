from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

from datasets import load_from_disk


ROOT = Path(__file__).resolve().parents[2]
SOURCE_COMMIT = "fabdc43ac2ae281262271aad2aadad488c76d667"
SOURCE_URL = f"https://raw.githubusercontent.com/Viendeptrai1/rethink-mcts-slm/{SOURCE_COMMIT}/data/humaneval/processed.jsonl"
SOURCE_SHA256 = "588938f21a6daf036f8bbce4b767c5c622802a8bbe90e809df61d1fb91fa9916"


def build_public_tests(raw: bytes, rows: list[dict]) -> list[dict]:
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("Pinned HumanEval source SHA-256 does not match")
    source_rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    if len(source_rows) != 164 or len(rows) != 164:
        raise ValueError("HumanEval source and local Arrow must each contain 164 rows")
    result: list[dict] = []
    for index, (source, local) in enumerate(zip(source_rows, rows)):
        if source.get("task_id") != f"Python/{index}" or local.get("task_id") != f"HumanEval/{index}":
            raise ValueError(f"HumanEval ID mismatch at {index}")
        if source.get("prompt") != local.get("prompt") or source.get("entry_point") != local.get("entry_point"):
            raise ValueError(f"HumanEval prompt or entry point differs at {index}")
        tests = source.get("given_tests")
        if not isinstance(tests, list) or not tests or not all(isinstance(item, str) and item.strip().startswith("assert ") for item in tests):
            raise ValueError(f"Missing or invalid public assertions at {index}")
        for assertion in tests:
            ast.parse(assertion)
        result.append({
            "task_id": local["task_id"],
            "entry_point": local["entry_point"],
            "given_tests": tests,
        })
    return result


def main() -> int:
    with urlopen(SOURCE_URL, timeout=30) as response:
        raw = response.read()
    rows = list(load_from_disk(str(ROOT / "data/humaneval/arrow"))["test"])
    public = build_public_tests(raw, rows)
    target = ROOT / "data/humaneval/public_tests.jsonl"
    content = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in public)
    if target.exists() and target.read_text(encoding="utf-8") != content:
        raise FileExistsError(f"Refusing to replace changed public tests: {target}")
    target.write_text(content, encoding="utf-8")
    provenance = ROOT / "data/humaneval/public_tests_source.json"
    metadata = {
        "source_url": SOURCE_URL, "source_commit": SOURCE_COMMIT,
        "source_sha256": SOURCE_SHA256, "public_tests_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "count": len(public),
    }
    serialized = json.dumps(metadata, indent=2) + "\n"
    if provenance.exists() and provenance.read_text(encoding="utf-8") != serialized:
        raise FileExistsError(f"Refusing to replace changed provenance: {provenance}")
    provenance.write_text(serialized, encoding="utf-8")
    print(f"Verified {len(public)} HumanEval public-test rows: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
