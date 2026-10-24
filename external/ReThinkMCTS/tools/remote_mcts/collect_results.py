from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from rethinkmcts.batch import ROOT, _safe_component


def collect_results(*, root: Path, run_name: str, model: str, partial: bool = False) -> Path:
    root = root.resolve()
    model_dir = _safe_component(model)
    artifacts = root / "outputs/rethinkmcts" / run_name / model_dir
    if not artifacts.is_dir():
        raise FileNotFoundError(artifacts)
    record = root / "outputs/benchmarks" / run_name / model_dir
    if not partial and not (record / "run.json").is_file():
        raise FileNotFoundError(f"Benchmark is not finalized: {record}")
    suffix = "checkpoint" if partial else "results"
    archive = root / "outputs/remote_mcts" / f"{run_name}_{model_dir}_{suffix}.zip"
    archive.parent.mkdir(parents=True, exist_ok=True)
    temporary = archive.with_suffix(".zip.tmp")
    with ZipFile(temporary, "w", compression=ZIP_DEFLATED, compresslevel=6) as output:
        for folder in (artifacts, root / "outputs/rethinkmcts_attempts" / run_name / model_dir, record):
            if folder.is_dir():
                for source in folder.rglob("*"):
                    if source.is_file():
                        output.write(source, source.relative_to(root).as_posix())
        worker_log = root / "outputs/remote_mcts/worker.log"
        if worker_log.is_file():
            output.write(worker_log, worker_log.relative_to(root).as_posix())
        output.writestr("result_bundle.json", json.dumps({
            "run_name": run_name, "model": model, "status": "partial" if partial else "complete",
        }, indent=2) + "\n")
    temporary.replace(archive)
    return archive


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Archive completed or partial remote MCTS artifacts")
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--partial", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    print(collect_results(root=args.root, run_name=args.run_name, model=args.model, partial=args.partial))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
