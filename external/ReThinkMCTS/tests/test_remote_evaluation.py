from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from tools.remote_evaluation import prepare_bundle
from tools.remote_evaluation.collect_results import collect_results


class RemoteEvaluationBundleTests(unittest.TestCase):
    def test_bundle_contains_only_selected_inputs_and_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            samples = {
                "apps": Path("data/samples/benchmark_v2/apps_test_300.json"),
                "humaneval": Path("data/samples/benchmark_v2/humaneval_test_164.json"),
            }
            for dataset, relative in samples.items():
                sample_path = root / relative
                sample_path.parent.mkdir(parents=True, exist_ok=True)
                sample_path.write_text(json.dumps({
                    "dataset": dataset, "split": "test", "sample_size": 1,
                    "problem_ids": [0],
                }), encoding="utf-8")
                problem_id = "0000" if dataset == "apps" else "HumanEval/0"
                candidate = (
                    root / "outputs/baselines/direct_generation/source/model" / dataset
                    / ("0000_timestamp" if dataset == "apps" else "HumanEval_0_timestamp")
                )
                candidate.mkdir(parents=True)
                (candidate / "solution.py").write_text("print(1)\n", encoding="utf-8")
                (candidate / "metadata.json").write_text(json.dumps({
                    "requested_model": "model",
                    "finish_reason": "stop",
                    "problem": {"dataset": dataset, "problem_id": problem_id, "split": "test"},
                }), encoding="utf-8")
                (candidate / "response.txt").write_text("do not transfer", encoding="utf-8")
            apps_test = root / "data/apps/raw/test/0000/input_output.json"
            apps_test.parent.mkdir(parents=True)
            apps_test.write_text('{"inputs":["1"],"outputs":["1"]}', encoding="utf-8")
            arrow = root / "data/humaneval/arrow/test/data.arrow"
            arrow.parent.mkdir(parents=True)
            arrow.write_bytes(b"arrow-test")
            tools_dir = root / "tools/remote_evaluation"
            tools_dir.mkdir(parents=True)
            for filename in ("Dockerfile", "requirements.txt", "run.sh"):
                (tools_dir / filename).write_text("test\n", encoding="utf-8")
            (root / ".env").write_text("SECRET=test\n", encoding="utf-8")
            archive = root / "out/bundle.zip"
            with patch.object(prepare_bundle, "SAMPLES", samples), patch.object(prepare_bundle, "CODE_DIRS", ()):
                info = prepare_bundle.create_bundle(
                    project_root=root, source_run="source", remote_run="new_run",
                    model="model", archive=archive,
                )
            self.assertEqual(info["candidate_counts"], {"apps": 1, "humaneval": 1})
            with ZipFile(archive) as bundle:
                names = set(bundle.namelist())
                self.assertIn("data/apps/raw/test/0000/input_output.json", names)
                self.assertIn("data/humaneval/arrow/test/data.arrow", names)
                self.assertIn("outputs/baselines/direct_generation/new_run/model/apps/0000_timestamp/solution.py", names)
                self.assertIn("outputs/baselines/direct_generation/new_run/model/humaneval/HumanEval_0_timestamp/metadata.json", names)
                self.assertFalse(any(name.endswith("response.txt") or name == ".env" for name in names))
                self.assertEqual(json.loads(bundle.read("bundle.json"))["run_name"], "new_run")

    def test_result_archive_includes_frozen_benchmark_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            reports = root / "outputs/baselines/evaluations/run/model"
            reports.mkdir(parents=True)
            (reports / "benchmark_summary.json").write_text("{}", encoding="utf-8")
            record = root / "outputs/benchmarks/run/model"
            record.mkdir(parents=True)
            (record / "run.json").write_text('{"status":"complete"}', encoding="utf-8")
            archive = collect_results(root, run_name="run", model="model")
            with ZipFile(archive) as output:
                self.assertIn("outputs/benchmarks/run/model/run.json", output.namelist())
                self.assertIn("outputs/baselines/evaluations/run/model/benchmark_summary.json", output.namelist())


if __name__ == "__main__":
    unittest.main()
