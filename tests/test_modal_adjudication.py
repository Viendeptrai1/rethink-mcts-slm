from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path
from unittest.mock import patch

from baselines.sample_selection import load_sample_manifest
from rethinkmcts.batch import ROOT, SAMPLES, _problem_key, _safe_component, _sha256
from rethinkmcts.config import SearchConfig
from tools.modal_mcts.adjudicate import finalize_adjudicated


class ModalAdjudicationTests(unittest.TestCase):
    def test_only_verified_missing_apps_count_as_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            model = "qwen2.5-coder:7b-instruct"
            model_dir = _safe_component(model)
            apps_run = "apps_parallel"
            humaneval_run = "humaneval_old"
            failures = {"0796", "1033", "1581"}
            manifests = {}
            for dataset, relative in SAMPLES.items():
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
                manifests[dataset] = load_sample_manifest(target, dataset=dataset)
            apps_ids = {_problem_key("apps", value) for value in manifests["apps"]["problem_ids"]}
            self.assertTrue(failures <= apps_ids)

            cohorts = {
                dataset: {
                    "manifest_sha256": _sha256(root / relative),
                    "test_data_sha256": "data",
                }
                for dataset, relative in SAMPLES.items()
            }
            for run_name in (apps_run, humaneval_run):
                run_dir = root / "outputs/rethinkmcts" / run_name / model_dir
                run_dir.mkdir(parents=True)
                (run_dir / "run_config.json").write_text(json.dumps({
                    "method": "RethinkMCTS", "run_name": run_name, "model": model,
                    "search": asdict(SearchConfig(run_name=run_name, model=model)),
                    "execution": {"source_sha256": "source", "provider": "modal_gpu", "model_digest": "digest"},
                    "cohorts": cohorts,
                }), encoding="utf-8")
            apps_dir = root / "outputs/rethinkmcts" / apps_run / model_dir
            progress = []
            for key in failures:
                for number in (1, 2):
                    attempt = root / "outputs/rethinkmcts_attempts" / apps_run / model_dir / "apps" / key / str(number)
                    attempt.mkdir(parents=True)
                    (attempt / "attempt.log").write_text("BATCH ERROR: test failure\n", encoding="utf-8")
                    progress.append({
                        "dataset": "apps", "problem_id": key,
                        "status": "timeout" if key == "1033" else "failed",
                        "error": "test failure", "attempt_dir": str(attempt),
                    })
            (apps_dir / "progress.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in progress), encoding="utf-8"
            )

            for dataset, manifest in manifests.items():
                run_name = apps_run if dataset == "apps" else humaneval_run
                config = asdict(SearchConfig(run_name=run_name, model=model))
                for problem_id in manifest["problem_ids"]:
                    key = _problem_key(dataset, problem_id)
                    if dataset == "apps" and key in failures:
                        continue
                    artifact = root / "outputs/rethinkmcts" / run_name / model_dir / dataset / _safe_component(key)
                    artifact.mkdir(parents=True)
                    (artifact / "final_solution.py").write_text("pass\n", encoding="utf-8")
                    (artifact / "search_summary.json").write_text(json.dumps({
                        "run_name": run_name, "model": model, "dataset": dataset,
                        "problem_id": key, "config": config,
                        "private_evaluation": {"status": "failed", "passed_tests": 0, "total_tests": 2},
                    }), encoding="utf-8")

            kwargs = dict(root=root, run_name=apps_run, humaneval_run_name=humaneval_run,
                          model=model, failed_apps=sorted(failures))
            with patch("tools.modal_mcts.adjudicate._source_hash", return_value="source"), patch(
                "tools.modal_mcts.adjudicate._data_hash", return_value="data"
            ):
                report = finalize_adjudicated(**kwargs)
                self.assertEqual(finalize_adjudicated(**kwargs), report)
                with self.assertRaisesRegex(ValueError, "Incomplete cohort without adjudication"):
                    finalize_adjudicated(**(kwargs | {"failed_apps": ["0796", "1033"]}))
            record = json.loads((report / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(record["coverage"]["apps"], {
                "expected": 300, "completed": 297, "adjudicated_failure": 3,
            })
            self.assertEqual(record["metrics"]["APPS Overall Pass@1 (%)"], 0.0)
            apps_rows = [json.loads(line) for line in (report / "apps/results.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(apps_rows), 300)
            self.assertEqual({row["problem_id"] for row in apps_rows if row["adjudicated_failure"]}, failures)
            self.assertEqual(len(record["adjudicated_failures"]), 3)


if __name__ == "__main__":
    unittest.main()
