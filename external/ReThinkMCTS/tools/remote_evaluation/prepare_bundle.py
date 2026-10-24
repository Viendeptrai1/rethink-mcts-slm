from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from baselines.direct_generation.pipeline import safe_path_component
from baselines.sample_selection import load_problem_ids, problem_keys
from evaluation.batch_evaluation import discover_candidates


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLES = {
    "apps": Path("data/samples/benchmark_v2/apps_test_300.json"),
    "humaneval": Path("data/samples/benchmark_v2/humaneval_test_164.json"),
}
CODE_DIRS = ("DataProcess", "Executors", "baselines", "evaluation", "tools/remote_evaluation")


def create_bundle(
    *,
    project_root: Path,
    source_run: str,
    remote_run: str,
    model: str,
    archive: Path,
    provider: str | None = None,
    model_revision: str | None = None,
    allow_missing: bool = False,
) -> dict[str, object]:
    project_root = project_root.resolve()
    archive = archive.resolve()
    if not source_run or not remote_run or safe_path_component(source_run) == remote_run:
        raise ValueError("Choose a distinct, non-empty remote run name to preserve the source run")
    if safe_path_component(remote_run) != remote_run:
        raise ValueError("Remote run name must be a safe directory name")
    if archive.exists():
        raise FileExistsError(f"Archive already exists: {archive}")

    selected: dict[str, list[tuple[Path, Path]]] = {}
    missing: dict[str, list[str]] = {}
    for dataset, sample_rel in SAMPLES.items():
        ids = load_problem_ids(project_root / sample_rel, dataset=dataset)
        candidates = discover_candidates(
            output_dir=project_root / "outputs/baselines",
            run_name=source_run,
            dataset=dataset,
            model=model,
            split="test",
            selected_problem_keys=problem_keys(project_root / sample_rel, dataset=dataset),
        )
        found = {candidate.problem_id for candidate in candidates}
        keys = {f"{value:04d}" if dataset == "apps" else f"HumanEval/{value}" for value in ids}
        missing[dataset] = sorted(keys - found)
        selected[dataset] = [(candidate.artifact_dir, Path(dataset) / candidate.artifact_dir.name) for candidate in candidates]

    if any(missing.values()) and not allow_missing:
        details = ", ".join(f"{name}: {len(values)} missing" for name, values in missing.items())
        raise ValueError(f"Incomplete generation ({details}); pass --allow-missing only for a partial audit")

    bundle_info: dict[str, object] = {
        "source_run": source_run,
        "run_name": remote_run,
        "model": model,
        "provider": provider,
        "model_revision": model_revision,
        "sample_ids": {name: len(load_problem_ids(project_root / rel, dataset=name)) for name, rel in SAMPLES.items()},
        "candidate_counts": {name: len(items) for name, items in selected.items()},
        "missing_ids": missing,
    }
    archive.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive, "x", compression=ZIP_DEFLATED, compresslevel=6) as output:
        for directory in CODE_DIRS:
            for source in (project_root / directory).rglob("*.py"):
                output.write(source, source.relative_to(project_root).as_posix())
        for filename in ("Dockerfile", "requirements.txt", "run.sh"):
            source = project_root / "tools/remote_evaluation" / filename
            output.write(source, source.relative_to(project_root).as_posix())
        for dataset, sample_rel in SAMPLES.items():
            output.write(project_root / sample_rel, sample_rel.as_posix())
            for source_dir, relative_dir in selected[dataset]:
                target = Path("outputs/baselines/direct_generation") / remote_run / safe_path_component(model) / relative_dir
                for filename in ("metadata.json", "solution.py"):
                    output.write(source_dir / filename, (target / filename).as_posix())
            if dataset == "apps":
                for problem_id in load_problem_ids(project_root / sample_rel, dataset=dataset):
                    source = project_root / "data/apps/raw/test" / f"{problem_id:04d}" / "input_output.json"
                    if not source.is_file():
                        raise FileNotFoundError(source)
                    output.write(source, source.relative_to(project_root).as_posix())
            else:
                source_root = project_root / "data/humaneval/arrow"
                if not source_root.is_dir():
                    raise FileNotFoundError(source_root)
                for source in source_root.rglob("*"):
                    if source.is_file():
                        output.write(source, source.relative_to(project_root).as_posix())
        output.writestr("bundle.json", json.dumps(bundle_info, indent=2) + "\n")
    return bundle_info


def main() -> int:
    parser = argparse.ArgumentParser(description="Package only benchmark-v2 inputs and generated code for remote evaluation")
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--source-run", required=True)
    parser.add_argument("--remote-run", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--provider", default=None, help="Non-secret provider label, e.g. ollama")
    parser.add_argument("--model-revision", default=None, help="Verified model weight digest/revision, if known")
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()
    info = create_bundle(
        project_root=args.project_root,
        source_run=args.source_run,
        remote_run=args.remote_run,
        model=args.model,
        archive=args.archive,
        provider=args.provider,
        model_revision=args.model_revision,
        allow_missing=args.allow_missing,
    )
    print(json.dumps(info, indent=2))
    print(f"Archive: {args.archive.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
