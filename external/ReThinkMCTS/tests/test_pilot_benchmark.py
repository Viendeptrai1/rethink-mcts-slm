from __future__ import annotations

import json
import hashlib
import tempfile
import unittest
from pathlib import Path

from rethinkmcts.pilot_benchmark import APPS_SAMPLE, HE_SAMPLE, build_pilot_report
from rethinkmcts.batch import _safe_component


class PilotBenchmarkTests(unittest.TestCase):
    def test_report_keeps_pilot_denominators_and_missing_candidates_visible(self):
        root = Path(__file__).resolve().parents[1]
        apps_manifest = root / APPS_SAMPLE
        he_manifest = root / HE_SAMPLE
        model = "qwen2.5-coder:7b-instruct"
        run = "synthetic_external_eval"
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            run_dir = temp_root / "outputs/rethinkmcts" / run / _safe_component(model)
            for dataset, manifest_path in (("apps", apps_manifest), ("humaneval", he_manifest)):
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                for index, problem_id in enumerate(manifest["problem_ids"]):
                    key = f"{problem_id:04d}" if dataset == "apps" else f"HumanEval/{problem_id}"
                    artifact = temp_root / "outputs/rethinkmcts" / run / _safe_component(model) / dataset / _safe_component(key)
                    artifact.mkdir(parents=True)
                    if dataset == "apps" and index == 0:
                        continue
                    (artifact / "final_solution.py").write_text("pass\n", encoding="utf-8")
                    (artifact / "search_summary.json").write_text(json.dumps({
                        "final_evaluation": {"passed_tests": 1, "total_tests": 1,
                                             "tests": [{"passed": True, "status": "passed"}]}
                    }), encoding="utf-8")
            config_path = run_dir / "run_config.json"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(json.dumps({
                "model": model,
                "search": {"evaluator_model": "qwen2.5-coder:14b-instruct"},
                "execution": {"model_digest": "gen", "evaluator_model_digest": "eval"},
                "cohorts": {
                    "apps": {"manifest_sha256": hashlib.sha256(apps_manifest.read_bytes()).hexdigest()},
                    "humaneval": {"manifest_sha256": hashlib.sha256(he_manifest.read_bytes()).hexdigest()},
                },
            }), encoding="utf-8")
            he_config_path = temp_root / "outputs/rethinkmcts" / run / _safe_component(model) / "run_config.json"
            he_config_path.write_text(config_path.read_text(encoding="utf-8"), encoding="utf-8")
            output = build_pilot_report(
                root=temp_root, run_name=run, model=model, apps_run_name=run,
                humaneval_run_name=run, apps_sample_file=apps_manifest,
                humaneval_sample_file=he_manifest, comparisons=[],
            )
            summary = json.loads((output / "benchmark_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "pilot")
            self.assertEqual(summary["cohorts"]["apps"]["sample_size"], 30)
            self.assertEqual(summary["cohorts"]["apps"]["missing_candidate_ids"], [f"{json.loads(apps_manifest.read_text())['problem_ids'][0]:04d}"])
            self.assertEqual(summary["methods"][0]["apps"]["groups"]["overall"]["expected_candidates"], 30)
            self.assertEqual(summary["methods"][0]["apps"]["groups"]["introductory"]["pass_at_1_percent"], 90.0)
            self.assertIn("n=30", summary["warning"])


if __name__ == "__main__":
    unittest.main()
