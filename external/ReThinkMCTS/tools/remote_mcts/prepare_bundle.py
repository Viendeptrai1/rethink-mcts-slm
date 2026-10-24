from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from baselines.sample_selection import load_sample_manifest
from rethinkmcts.batch import ROOT, SAMPLES, _data_hash, _sha256, _source_hash, _safe_component, validate_cohort


CODE_DIRS = ("rethinkmcts", "ChatModels", "DataProcess", "Executors", "baselines", "evaluation", "tools/remote_mcts", "tools/gpu")


def create_bundle(*, root: Path, run_name: str, model: str, archive: Path) -> dict[str, object]:
    root = root.resolve()
    archive = archive.resolve()
    if archive.exists():
        raise FileExistsError(f"Bundle already exists: {archive}")
    if _safe_component(run_name) != run_name:
        raise ValueError("Unsafe run name")
    manifests = {dataset: load_sample_manifest(root / relative, dataset=dataset) for dataset, relative in SAMPLES.items()}
    validate_cohort(manifests)
    selected_files: list[Path] = []
    for problem_id in manifests["apps"]["problem_ids"]:
        folder = root / "data/apps/raw/test" / f"{problem_id:04d}"
        selected_files.extend((folder / "question.txt", folder / "input_output.json"))
        starter = folder / "starter_code.py"
        if starter.is_file():
            selected_files.append(starter)
    selected_files.extend(path for path in (root / "data/humaneval/arrow").rglob("*") if path.is_file())
    selected_files.extend((root / "data/humaneval/public_tests.jsonl", root / "data/humaneval/public_tests_source.json"))
    for path in selected_files:
        if not path.is_file():
            raise FileNotFoundError(path)
    info: dict[str, object] = {
        "schema_version": 1,
        "method": "RethinkMCTS",
        "run_name": run_name,
        "model": model,
        "cohorts": {dataset: {
            "sample_id": manifest["sample_id"],
            "count": len(manifest["problem_ids"]),
            "manifest_sha256": _sha256(root / SAMPLES[dataset]),
            "test_data_sha256": _data_hash(root, dataset, manifest["problem_ids"]),
        } for dataset, manifest in manifests.items()},
        "source_sha256": _source_hash(root),
        "data_file_count": len(selected_files),
        "data_bytes": sum(path.stat().st_size for path in selected_files),
    }
    archive.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive, "x", compression=ZIP_DEFLATED, compresslevel=6) as output:
        for directory in CODE_DIRS:
            for source in (root / directory).rglob("*.py"):
                output.write(source, source.relative_to(root).as_posix())
        for filename in ("Dockerfile", "requirements.txt", "run.sh"):
            source = root / "tools/remote_mcts" / filename
            output.write(source, source.relative_to(root).as_posix())
        for relative in SAMPLES.values():
            output.write(root / relative, relative.as_posix())
        for source in selected_files:
            output.write(source, source.relative_to(root).as_posix())
        output.writestr("bundle.json", json.dumps(info, ensure_ascii=False, indent=2) + "\n")
    return info


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Package exact 300+164 MCTS cohort without reference solutions or secrets")
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--model", default="qwen2.5-coder:7b-instruct")
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    print(json.dumps(create_bundle(root=args.root, run_name=args.run_name, model=args.model, archive=args.archive), indent=2))
    print(f"Archive: {args.archive.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
