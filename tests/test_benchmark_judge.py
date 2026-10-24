from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evaluation.benchmark_judge import aggregate_group, build_table, write_judge_report


class BenchmarkJudgeTests(unittest.TestCase):
    def test_apps_metrics_include_missing_and_use_macro_rate(self) -> None:
        rows = {
            "0000": {
                "problem_id": "0000",
                "failure_type": "passed",
                "passed_tests": 2,
                "total_tests": 2,
                "pass_rate": 1.0,
            },
            "0001": {
                "problem_id": "0001",
                "failure_type": "wrong_answer",
                "passed_tests": 1,
                "total_tests": 4,
                "pass_rate": 0.25,
            },
        }
        result = aggregate_group(
            group="overall",
            problem_ids=[0, 1, 2],
            rows=rows,
            dataset="apps",
            difficulty_map={"0": "introductory", "1": "interview", "2": "competition"},
        )
        self.assertEqual(result["expected_candidates"], 3)
        self.assertEqual(result["missing_candidates"], 1)
        self.assertAlmostEqual(result["pass_rate_percent"], 41.666666, places=4)
        self.assertAlmostEqual(result["micro_pass_rate_percent"], 50.0, places=4)
        self.assertAlmostEqual(result["pass_at_1_percent"], 33.333333, places=4)

    def test_humaneval_has_no_pass_rate(self) -> None:
        result = aggregate_group(
            group="overall",
            problem_ids=[0, 1],
            rows={
                "HumanEval/0": {
                    "failure_type": "passed",
                    "passed_tests": 1,
                    "total_tests": 1,
                    "pass_rate": 1.0,
                }
            },
            dataset="humaneval",
        )
        self.assertIsNone(result["pass_rate_percent"])
        self.assertAlmostEqual(result["pass_at_1_percent"], 50.0)

    def test_write_report_creates_paper_style_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            apps_sample = root / "apps.json"
            humaneval_sample = root / "humaneval.json"
            apps_sample.write_text(
                json.dumps(
                    {
                        "sample_id": "test",
                        "dataset": "apps",
                        "split": "test",
                        "seed": 1,
                        "population_size": 5000,
                        "sample_size": 3,
                        "problem_ids": [0, 1, 2],
                        "difficulty_by_problem_id": {
                            "0": "introductory",
                            "1": "interview",
                            "2": "competition",
                        },
                    }
                ),
                encoding="utf-8",
            )
            humaneval_sample.write_text(
                json.dumps(
                    {
                        "sample_id": "test",
                        "dataset": "humaneval",
                        "split": "test",
                        "seed": 2,
                        "population_size": 164,
                        "sample_size": 2,
                        "problem_ids": [0, 1],
                    }
                ),
                encoding="utf-8",
            )
            model_dir = root / "evaluations" / "run" / "model"
            (model_dir / "apps").mkdir(parents=True)
            (model_dir / "humaneval").mkdir(parents=True)
            (model_dir / "apps" / "results.jsonl").write_text(
                "\n".join(
                    json.dumps(row)
                    for row in [
                        {"problem_id": "0000", "failure_type": "passed", "passed_tests": 1, "total_tests": 1, "pass_rate": 1.0},
                        {"problem_id": "0001", "failure_type": "wrong_answer", "passed_tests": 0, "total_tests": 2, "pass_rate": 0.0},
                        {"problem_id": "0002", "failure_type": "passed", "passed_tests": 3, "total_tests": 3, "pass_rate": 1.0},
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (model_dir / "humaneval" / "results.jsonl").write_text(
                json.dumps({"problem_id": "HumanEval/0", "failure_type": "passed", "passed_tests": 1, "total_tests": 1, "pass_rate": 1.0})
                + "\n",
                encoding="utf-8",
            )
            summary = write_judge_report(
                output_dir=root,
                run_name="run",
                model="model",
                apps_sample_file=apps_sample,
                humaneval_sample_file=humaneval_sample,
                method="Direct Evaluation",
            )
            self.assertEqual(summary["table"]["APPS Overall Pass@1 (%)"], 66.67)
            self.assertEqual(summary["table"]["HumanEval Pass Rate (%)"], "N/A")
            self.assertTrue((model_dir / "benchmark_table.md").is_file())
            self.assertTrue((model_dir / "apps" / "benchmark_metrics.json").is_file())


if __name__ == "__main__":
    unittest.main()
