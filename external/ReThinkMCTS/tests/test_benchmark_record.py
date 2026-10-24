from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from evaluation.benchmark_record import create_record
from evaluation.compare_benchmarks import compare_records


def prepare_fake_run(root: Path) -> Path:
    run = "new_run"
    model = "model"
    base = root / "outputs/baselines/evaluations" / run / model
    datasets = {}
    for dataset in ("apps", "humaneval"):
        relative = Path("data/samples/benchmark_v2") / ("apps_test_300.json" if dataset == "apps" else "humaneval_test_164.json")
        sample = {
            "sample_id": f"test_{dataset}", "dataset": dataset, "split": "test",
            "seed": 1, "population_size": 5000 if dataset == "apps" else 164,
            "sample_size": 1, "problem_ids": [0],
        }
        if dataset == "apps":
            sample["difficulty_by_problem_id"] = {"0": "introductory"}
        sample_path = root / relative
        sample_path.parent.mkdir(parents=True, exist_ok=True)
        sample_path.write_text(json.dumps(sample), encoding="utf-8")
        if dataset == "apps":
            tests = root / "data/apps/raw/test/0000/input_output.json"
            tests.parent.mkdir(parents=True, exist_ok=True)
            tests.write_text('{"inputs":["1"],"outputs":["1"]}', encoding="utf-8")
        else:
            arrow = root / "data/humaneval/arrow/test/data.arrow"
            arrow.parent.mkdir(parents=True, exist_ok=True)
            arrow.write_bytes(b"arrow-test")
        problem_id = "0000" if dataset == "apps" else "HumanEval/0"
        candidate = root / "outputs/baselines/direct_generation" / run / model / dataset / ("0000_now" if dataset == "apps" else "HumanEval_0_now")
        candidate.mkdir(parents=True)
        (candidate / "solution.py").write_text("print(1)\n", encoding="utf-8")
        (candidate / "evaluation.json").write_text(json.dumps({
            "passed_tests": 1, "total_tests": 1,
            "evaluation_provenance": {
                "solution_sha256": hashlib.sha256((candidate / "solution.py").read_bytes()).hexdigest(),
                "timeout_seconds": 2.0, "test_workers": 1, "max_tests": None,
            },
        }), encoding="utf-8")
        (candidate / "metadata.json").write_text(json.dumps({
            "run_name": "source_run", "requested_model": model, "response_model": model,
            "finish_reason": "stop", "generation": {"prompt_version": "v1", "max_tokens": 2048},
            "usage": {"total_tokens": 100},
            "problem": {"dataset": dataset, "problem_id": problem_id, "split": "test"},
        }), encoding="utf-8")
        folder = base / dataset
        folder.mkdir(parents=True)
        (folder / "results.jsonl").write_text(json.dumps({
            "problem_id": problem_id, "failure_type": "passed", "passed_tests": 1, "total_tests": 1,
        }) + "\n", encoding="utf-8")
        (folder / "summary.json").write_text(json.dumps({
            "run_name": run, "model": model,
            "evaluation_config": {
                "split": "test", "workers": 2, "test_workers": 1,
                "timeout_seconds": 2.0, "max_tests": None,
                "timeout_scope": "per_test" if dataset == "apps" else "official_harness",
                "test_policy": "all_input_output_cases" if dataset == "apps" else "official_harness",
                "sample_manifest": str(sample_path),
                "sample_manifest_sha256": hashlib.sha256(sample_path.read_bytes()).hexdigest(),
            },
        }), encoding="utf-8")
        datasets[dataset] = {
            "sample_manifest": sample,
            "groups": {"overall": {
                "expected_candidates": 1, "missing_candidates": 0,
                "difficulty_counts": {"introductory": 1} if dataset == "apps" else None,
            }},
        }
    base.mkdir(parents=True, exist_ok=True)
    (base / "benchmark_summary.json").write_text(json.dumps({
        "run_name": run, "model": model, "method": "Direct Evaluation", "datasets": datasets,
        "table": {"Method": "Direct Evaluation", "APPS Overall Pass@1 (%)": 100.0},
    }), encoding="utf-8")
    (base / "benchmark_table.csv").write_text("Method\nDirect Evaluation\n", encoding="utf-8")
    (base / "benchmark_table.md").write_text("| Method |\n| --- |\n| Direct Evaluation |\n", encoding="utf-8")
    remote = root / "tools/remote_evaluation"
    remote.mkdir(parents=True)
    for filename in ("Dockerfile", "requirements.txt", "run.sh"):
        (remote / filename).write_text("test\n", encoding="utf-8")
    bundle = root / "bundle.json"
    bundle.write_text(json.dumps({
        "run_name": run, "model": model, "source_run": "source_run", "provider": "ollama",
    }), encoding="utf-8")
    return bundle


class BenchmarkRecordTests(unittest.TestCase):
    def test_freezes_actual_configuration_and_refuses_changed_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle = prepare_fake_run(root)
            path = create_record(root=root, bundle_file=bundle)
            record = json.loads((path / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(record["status"], "complete")
            self.assertEqual(record["provider"], "ollama")
            self.assertEqual(record["evaluation"]["apps"]["timeout_seconds"], 2.0)
            self.assertEqual(record["coverage"]["humaneval"]["evaluated"], 1)
            self.assertEqual(len((path / "candidates.csv").read_text(encoding="utf-8").splitlines()), 3)
            self.assertTrue((path / "apps/results.jsonl").is_file())
            self.assertEqual(create_record(root=root, bundle_file=bundle), path)
            results = root / "outputs/baselines/evaluations/new_run/model/apps/results.jsonl"
            results.write_text(results.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                create_record(root=root, bundle_file=bundle)

    def test_incomplete_evaluation_cannot_be_finalized(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle = prepare_fake_run(root)
            results = root / "outputs/baselines/evaluations/new_run/model/humaneval/results.jsonl"
            results.write_text("", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "incomplete"):
                create_record(root=root, bundle_file=bundle)
            self.assertFalse((root / "outputs/benchmarks/new_run/model").exists())

    def test_changed_timeout_or_solution_cannot_be_finalized(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle = prepare_fake_run(root)
            candidate = root / "outputs/baselines/direct_generation/new_run/model/apps/0000_now"
            candidate.joinpath("solution.py").write_text("print(2)\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "different code or settings"):
                create_record(root=root, bundle_file=bundle)
            candidate.joinpath("solution.py").write_text("print(1)\n", encoding="utf-8")
            summary = root / "outputs/baselines/evaluations/new_run/model/apps/summary.json"
            value = json.loads(summary.read_text(encoding="utf-8"))
            value["evaluation_config"]["timeout_seconds"] = 10.0
            summary.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "different code or settings"):
                create_record(root=root, bundle_file=bundle)

    def test_comparison_requires_same_cohort_and_judge_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = []
            for index in (1, 2):
                record = {
                    "status": "complete", "run_name": f"run_{index}", "model": f"model_{index}",
                    "method": "Direct Evaluation", "provider": "ollama", "source_generation_run": "source",
                    "generation_profiles": [{"max_tokens": 2048}],
                    "cohorts": {dataset: {"manifest_sha256": "same", "test_data_sha256": "same_data"} for dataset in ("apps", "humaneval")},
                    "evaluation": {dataset: {"test_policy": "all", "timeout_seconds": 2.0, "max_tests": None, "workers": 2} for dataset in ("apps", "humaneval")},
                    "execution": {"python_version": "3.11", "site": "ckey", "backend": "docker", "image_id": "sha256:test", "code_sha256": "code"},
                    "metrics": {"APPS Overall Pass@1 (%)": 50.0 + index},
                }
                path = root / f"record_{index}.json"
                path.write_text(json.dumps(record), encoding="utf-8")
                files.append(path)
            output = compare_records(record_files=files, name="comparison_v1", root=root)
            self.assertTrue((output / "comparison.csv").is_file())
            self.assertEqual(compare_records(record_files=files, name="comparison_v1", root=root), output)
            changed = json.loads(files[1].read_text(encoding="utf-8"))
            changed["cohorts"]["apps"]["manifest_sha256"] = "different"
            files[1].write_text(json.dumps(changed), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Incompatible"):
                compare_records(record_files=files, name="other", root=root)


if __name__ == "__main__":
    unittest.main()
