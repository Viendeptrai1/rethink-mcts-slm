from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from baselines.direct_generation.pipeline import safe_path_component


def collect_results(root: Path, *, run_name: str, model: str) -> Path:
    run_dir = safe_path_component(run_name)
    model_dir = safe_path_component(model)
    base = root / "outputs/baselines"
    reports = base / "evaluations" / run_dir / model_dir
    if not (reports / "benchmark_summary.json").is_file():
        raise FileNotFoundError(f"Benchmark summary not found: {reports}")
    record_dir = root / "outputs/benchmarks" / run_dir / model_dir
    if not (record_dir / "run.json").is_file():
        raise FileNotFoundError(f"Final benchmark record not found: {record_dir}")
    target = root / "outputs/remote_evaluation" / f"{run_dir}_{model_dir}_results.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, "w", compression=ZIP_DEFLATED) as output:
        for source in reports.rglob("*"):
            if source.is_file():
                output.write(source, source.relative_to(root).as_posix())
        for source in (base / "direct_generation" / run_dir / model_dir).glob("*/*/evaluation.json"):
            output.write(source, source.relative_to(root).as_posix())
        for source in record_dir.rglob("*"):
            if source.is_file():
                output.write(source, source.relative_to(root).as_posix())
        worker_log = root / "outputs/remote_evaluation/worker.log"
        if worker_log.is_file():
            output.write(worker_log, worker_log.relative_to(root).as_posix())
        output.writestr(
            "result_bundle.json",
            json.dumps({"run_name": run_name, "model": model}, indent=2) + "\n",
        )
    return target
