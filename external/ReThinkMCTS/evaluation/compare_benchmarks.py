from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from baselines.direct_generation.pipeline import safe_path_component


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASETS = ("apps", "humaneval")


def _comparison_policy(record: dict[str, Any]) -> dict[str, Any]:
    return {
        dataset: {
            "manifest_sha256": record["cohorts"][dataset]["manifest_sha256"],
            "test_data_sha256": record["cohorts"][dataset]["test_data_sha256"],
            "test_policy": record["evaluation"][dataset]["test_policy"],
            "timeout_seconds": record["evaluation"][dataset]["timeout_seconds"],
            "max_tests": record["evaluation"][dataset]["max_tests"],
        }
        for dataset in DATASETS
    } | {"python_version": record["execution"]["python_version"]}


def compare_records(*, record_files: list[Path], name: str, root: Path) -> Path:
    if len(record_files) < 2:
        raise ValueError("At least two benchmark records are required")
    if safe_path_component(name) != name:
        raise ValueError("Comparison name must be a safe directory name")
    records = [json.loads(path.read_text(encoding="utf-8")) for path in record_files]
    if any(record.get("status") != "complete" for record in records):
        raise ValueError("Only complete benchmark records can be compared")
    policy = _comparison_policy(records[0])
    for record in records[1:]:
        if _comparison_policy(record) != policy:
            raise ValueError(f"Incompatible cohort, test policy, timeout or Python version: {record['run_name']}")

    metrics = list(records[0]["metrics"])
    for record in records[1:]:
        if set(record["metrics"]) != set(metrics):
            raise ValueError("Benchmark metric columns differ")
    columns = [
        "run_name", "model", "model_revision", "method", "provider", "source_generation_run",
        "generation_profiles", "apps_workers", "humaneval_workers", "execution_site",
        "backend", "image_id", "code_sha256", *metrics,
    ]
    rows = []
    for record in records:
        rows.append({
            "run_name": record["run_name"],
            "model": record["model"],
            "model_revision": record.get("model_revision"),
            "method": record["method"],
            "provider": record.get("provider"),
            "source_generation_run": record.get("source_generation_run"),
            "generation_profiles": json.dumps(record["generation_profiles"], sort_keys=True),
            "apps_workers": record["evaluation"]["apps"]["workers"],
            "humaneval_workers": record["evaluation"]["humaneval"]["workers"],
            "execution_site": record["execution"]["site"],
            "backend": record["execution"]["backend"],
            "image_id": record["execution"].get("image_id"),
            "code_sha256": record["execution"]["code_sha256"],
            **record["metrics"],
        })
    input_hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in record_files]
    fingerprint = hashlib.sha256(json.dumps(input_hashes, sort_keys=True).encode("utf-8")).hexdigest()
    target = root.resolve() / "outputs/benchmarks/comparisons" / name
    if target.exists():
        previous = json.loads((target / "comparison.json").read_text(encoding="utf-8"))
        if previous.get("source_fingerprint") == fingerprint:
            return target
        raise FileExistsError(f"Comparison already exists with different records: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{name}.", dir=target.parent))
    try:
        with (staging / "comparison.csv").open("w", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
        with (staging / "comparison.md").open("w", encoding="utf-8") as output:
            output.write("| " + " | ".join(columns) + " |\n")
            output.write("| " + " | ".join("---" for _ in columns) + " |\n")
            for row in rows:
                output.write("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |\n")
        (staging / "comparison.json").write_text(json.dumps({
            "schema_version": 1,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "name": name,
            "record_files": [str(path.resolve()) for path in record_files],
            "comparison_policy": policy,
            "source_hashes": input_hashes,
            "source_fingerprint": fingerprint,
            "rows": rows,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        staging.rename(target)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare complete benchmark records with matching cohorts and judge policy")
    parser.add_argument("--name", required=True)
    parser.add_argument("--records", type=Path, nargs="+", required=True)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    args = parser.parse_args(argv)
    print(compare_records(record_files=args.records, name=args.name, root=args.root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
