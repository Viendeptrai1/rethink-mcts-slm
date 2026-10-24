from __future__ import annotations

import json
import io
import shutil
import tempfile
import unittest
from dataclasses import asdict
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from baselines.sample_selection import load_sample_manifest
from rethinkmcts import batch
from rethinkmcts.benchmark import finalize_benchmark
from rethinkmcts.config import SearchConfig
from rethinkmcts.runner import load_context
from tools.remote_mcts.prepare_bundle import create_bundle


class RemoteMCTSTests(unittest.TestCase):
    def test_all_humaneval_tasks_have_pinned_public_tests(self):
        source = batch.ROOT / "data/humaneval/public_tests.jsonl"
        rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(rows), 164)
        self.assertTrue(all(row["given_tests"] for row in rows))
        for problem_id in (0, 63, 163):
            context = load_context("humaneval", problem_id)
            self.assertEqual(context.public_test_count, len(rows[problem_id]["given_tests"]))
            self.assertEqual(context.public_tests, tuple(rows[problem_id]["given_tests"]))

    def test_humaneval_missing_public_tests_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "humaneval").mkdir()
            with patch("datasets.load_from_disk", return_value={"test": [{"task_id": "HumanEval/0", "prompt": "x", "entry_point": "f"}]}):
                with self.assertRaises(FileNotFoundError):
                    load_context("humaneval", 0, data_root=root)

    def test_humaneval_public_test_identity_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "humaneval"
            folder.mkdir()
            (folder / "public_tests.jsonl").write_text(json.dumps({
                "task_id": "HumanEval/999", "entry_point": "f", "given_tests": ["assert f()"]
            }) + "\n", encoding="utf-8")
            with patch("datasets.load_from_disk", return_value={"test": [{"task_id": "HumanEval/0", "prompt": "x", "entry_point": "f"}]}):
                with self.assertRaisesRegex(ValueError, "identity mismatch"):
                    load_context("humaneval", 0, data_root=root)

    def test_bundle_contains_exact_cohort_and_no_secrets_or_reference_solutions(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "mcts.zip"
            info = create_bundle(root=batch.ROOT, run_name="test_mcts_bundle", model="qwen2.5-coder:7b-instruct", archive=archive)
            self.assertEqual(info["cohorts"]["apps"]["count"], 300)
            self.assertEqual(info["cohorts"]["humaneval"]["count"], 164)
            self.assertEqual(len(info["cohorts"]["apps"]["test_data_sha256"]), 64)
            self.assertEqual(len(info["cohorts"]["humaneval"]["test_data_sha256"]), 64)
            with ZipFile(archive) as source:
                names = set(source.namelist())
                self.assertIn("data/humaneval/public_tests.jsonl", names)
                self.assertIn("data/humaneval/public_tests_source.json", names)
                self.assertIn("rethinkmcts/batch.py", names)
                self.assertIn("tools/remote_mcts/run_bundle.py", names)
                self.assertNotIn(".env", names)
                self.assertFalse(any(name.endswith("solution.py") or name.startswith("outputs/") for name in names))
                self.assertEqual(len([name for name in names if name.endswith("/question.txt")]), 300)

    def test_batch_plan_selects_300_plus_164_without_llm(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("rethinkmcts.batch._run_one", side_effect=AssertionError("must not run")):
                status = batch.main([
                    "--run-name", "test_plan", "--model", "qwen2.5-coder:7b-instruct",
                    "--output-root", str(Path(directory) / "mcts"),
                    "--attempt-root", str(Path(directory) / "attempts"), "--plan",
                ])
            self.assertEqual(status, 0)
            self.assertFalse(list(Path(directory).rglob("run_config.json")))

    def test_locked_external_evaluator_pilot_manifest_is_10_per_difficulty(self):
        manifest = load_sample_manifest(
            batch.ROOT / "data/samples/benchmark_v2/apps_test_30_external_evaluator_pilot.json",
            dataset="apps",
        )
        counts = {difficulty: sum(manifest["difficulty_by_problem_id"][str(pid)] == difficulty
                                  for pid in manifest["problem_ids"])
                  for difficulty in ("introductory", "interview", "competition")}
        self.assertEqual(len(manifest["problem_ids"]), 30)
        self.assertEqual(counts, {"introductory": 10, "interview": 10, "competition": 10})
        manifests = {
            "apps": manifest,
            "humaneval": load_sample_manifest(batch.ROOT / batch.SAMPLES["humaneval"], dataset="humaneval"),
        }
        batch.validate_cohort(manifests)

    def test_batch_plan_selects_fixed_apps_pilot(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(batch.main([
                "--dataset", "apps", "--apps-sample-file",
                "data/samples/benchmark_v2/apps_test_30_external_evaluator_pilot.json",
                "--run-name", "external_eval_pilot_plan", "--model", "qwen2.5-coder:7b-instruct",
                "--evaluator-model", "qwen2.5-coder:14b-instruct", "--workers", "4", "--plan",
            ]), 0)
        plan = json.loads(output.getvalue())
        self.assertEqual(plan["selected"], {"apps": 30})
        self.assertEqual(plan["evaluator_model"], "qwen2.5-coder:14b-instruct")

    def test_batch_plan_selects_only_requested_cohort_ids(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(batch.main([
                "--dataset", "apps", "--problem-ids", "1684", "3702",
                "--run-name", "ast_repair_plan", "--model", "qwen2.5-coder:7b-instruct",
                "--plan",
            ]), 0)
        plan = json.loads(output.getvalue())
        self.assertEqual(plan["selected"], {"apps": 2})
        self.assertEqual(plan["pending"], 2)
        with self.assertRaisesRegex(ValueError, "outside the locked"):
            batch.main([
                "--dataset", "apps", "--problem-ids", "999999",
                "--run-name", "ast_repair_plan", "--model", "qwen2.5-coder:7b-instruct",
                "--plan",
            ])

    def test_batch_rejects_unconfirmed_full_run(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(SystemExit, "Refusing more than two"):
                batch.main([
                    "--run-name", "test_gate", "--model", "qwen2.5-coder:7b-instruct",
                    "--output-root", str(Path(directory) / "mcts"),
                    "--attempt-root", str(Path(directory) / "attempts"),
                ])
            self.assertFalse(list(Path(directory).rglob("run_config.json")))

    def test_batch_resumes_complete_problem_and_rejects_changed_search(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            arguments = [
                "--dataset", "humaneval", "--limit", "1", "--run-name", "resume_test",
                "--model", "qwen2.5-coder:7b-instruct",
                "--output-root", str(root / "mcts"),
                "--attempt-root", str(root / "attempts"),
            ]

            def completed(args, config, dataset, key, number):
                artifact = args.output_root / args.run_name / batch._safe_component(args.model) / dataset / batch._safe_component(key)
                artifact.mkdir(parents=True)
                (artifact / "search_summary.json").write_text(json.dumps({
                    "run_name": args.run_name, "model": args.model, "dataset": dataset,
                    "problem_id": key, "config": config["search"],
                }), encoding="utf-8")
                (artifact / "final_solution.py").write_text("pass\n", encoding="utf-8")
                return {"dataset": dataset, "problem_id": key, "status": "completed"}

            with patch("rethinkmcts.batch._run_one", side_effect=completed) as runner:
                self.assertEqual(batch.main(arguments), 0)
                self.assertEqual(runner.call_count, 1)
            with patch("rethinkmcts.batch._run_one", side_effect=AssertionError("should skip")):
                self.assertEqual(batch.main(arguments), 0)
            with self.assertRaisesRegex(ValueError, "different identity or parameters"):
                batch.main([*arguments, "--rollouts", "3"])

    def test_batch_parallel_searches_unique_problems_and_resumes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            arguments = [
                "--dataset", "humaneval", "--limit", "4", "--workers", "2",
                "--run-name", "parallel_test", "--model", "qwen2.5-coder:7b-instruct",
                "--output-root", str(root / "mcts"), "--attempt-root", str(root / "attempts"),
                "--confirm-full-run",
            ]
            seen = []

            def completed(args, config, dataset, key, number):
                seen.append(key)
                artifact = args.output_root / args.run_name / batch._safe_component(args.model) / dataset / batch._safe_component(key)
                artifact.mkdir(parents=True)
                (artifact / "search_summary.json").write_text(json.dumps({
                    "run_name": args.run_name, "model": args.model, "dataset": dataset,
                    "problem_id": key, "config": config["search"],
                }), encoding="utf-8")
                (artifact / "final_solution.py").write_text("pass\n", encoding="utf-8")
                return {"dataset": dataset, "problem_id": key, "status": "completed"}

            with patch("rethinkmcts.batch._run_one", side_effect=completed):
                self.assertEqual(batch.main(arguments), 0)
            self.assertEqual(len(seen), 4)
            self.assertEqual(len(set(seen)), 4)
            with patch("rethinkmcts.batch._run_one", side_effect=AssertionError("should skip")):
                self.assertEqual(batch.main(arguments), 0)
            progress = (root / "mcts/parallel_test/qwen2.5-coder_7b-instruct/progress.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(progress), 4)
            with self.assertRaisesRegex(ValueError, "Run parameters, cohort, model or code changed"):
                batch.main([*arguments, "--workers", "3"])

    def test_finalizer_aggregates_complete_cohort_and_rejects_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            samples = {}
            for dataset, relative in batch.SAMPLES.items():
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(batch.ROOT / relative, target)
                samples[dataset] = json.loads(target.read_text(encoding="utf-8"))
            run_name = "fake_mcts"
            model = "qwen2.5-coder:7b-instruct"
            model_dir = batch._safe_component(model)
            run_dir = root / "outputs/rethinkmcts" / run_name / model_dir
            config = asdict(SearchConfig(run_name=run_name, model=model))
            record = {
                "method": "RethinkMCTS", "run_name": run_name, "model": model,
                "search": config,
                "batch": {"problem_timeout_seconds": 900},
                "execution": {"source_sha256": "source", "python_version": "3.11", "model_digest": "digest", "image_id": "image"},
                "cohorts": {dataset: {
                    "manifest_sha256": batch._sha256(root / relative),
                    "test_data_sha256": "data",
                    "sample_id": samples[dataset]["sample_id"],
                } for dataset, relative in batch.SAMPLES.items()},
            }
            run_dir.mkdir(parents=True)
            (run_dir / "run_config.json").write_text(json.dumps(record), encoding="utf-8")
            for dataset, manifest in samples.items():
                for index, problem_id in enumerate(manifest["problem_ids"]):
                    key = batch._problem_key(dataset, problem_id)
                    artifact = run_dir / dataset / batch._safe_component(key)
                    artifact.mkdir(parents=True)
                    passed, total = (2, 2) if index == 0 else (1, 2) if dataset == "apps" and index == 1 else (0, 2)
                    if dataset == "humaneval":
                        passed, total = (1, 1) if index == 0 else (0, 1)
                    summary = {
                        "run_name": run_name, "model": model, "dataset": dataset,
                        "problem_id": key, "config": config, "best_reward": 0.5,
                        "best_candidate_id": "candidate_0001", "request_count": 3,
                        "token_usage": {"total_tokens": 30},
                        "private_evaluation": {
                            "status": "passed" if passed == total else "failed",
                            "passed_tests": passed, "total_tests": total,
                            "tests": [],
                        },
                    }
                    (artifact / "search_summary.json").write_text(json.dumps(summary), encoding="utf-8")
                    (artifact / "final_solution.py").write_text("pass\n", encoding="utf-8")
            with patch("rethinkmcts.benchmark._source_hash", return_value="source"), patch("rethinkmcts.benchmark._data_hash", return_value="data"):
                missing = run_dir / "apps" / batch._safe_component(batch._problem_key("apps", samples["apps"]["problem_ids"][-1])) / "search_summary.json"
                missing.unlink()
                with self.assertRaisesRegex(ValueError, "Incomplete MCTS cohort"):
                    finalize_benchmark(root=root, run_name=run_name, model=model)
                missing.write_text(json.dumps(summary | {"dataset": "apps", "problem_id": batch._problem_key("apps", samples["apps"]["problem_ids"][-1]), "private_evaluation": {"status": "failed", "passed_tests": 0, "total_tests": 2}}), encoding="utf-8")
                target = finalize_benchmark(root=root, run_name=run_name, model=model)
            output = json.loads((target / "benchmark_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(output["datasets"]["apps"]["groups"]["overall"]["expected_candidates"], 300)
            self.assertEqual(output["datasets"]["apps"]["groups"]["overall"]["difficulty_counts"], {"introductory": 100, "interview": 100, "competition": 100})
            self.assertAlmostEqual(output["table"]["APPS Overall Pass Rate (%)"], 0.5)
            self.assertEqual(output["table"]["HumanEval Pass Rate (%)"], "N/A")
            self.assertAlmostEqual(output["table"]["HumanEval Pass@1 (%)"], 0.61)

            parallel_name = "fake_parallel"
            parallel_dir = root / "outputs/rethinkmcts" / parallel_name / model_dir
            parallel_dir.mkdir(parents=True)
            parallel_config = json.loads(json.dumps(record))
            parallel_config["run_name"] = parallel_name
            parallel_config["search"]["run_name"] = parallel_name
            parallel_config["batch"]["workers"] = 4
            (parallel_dir / "run_config.json").write_text(json.dumps(parallel_config), encoding="utf-8")
            shutil.copytree(run_dir / "apps", parallel_dir / "apps")
            for summary_path in (parallel_dir / "apps").glob("*/search_summary.json"):
                value = json.loads(summary_path.read_text(encoding="utf-8"))
                value["run_name"] = parallel_name
                value["config"]["run_name"] = parallel_name
                summary_path.write_text(json.dumps(value), encoding="utf-8")
            with patch("rethinkmcts.benchmark._source_hash", return_value="source"), patch("rethinkmcts.benchmark._data_hash", return_value="data"):
                joined = finalize_benchmark(root=root, run_name=parallel_name, model=model,
                                            humaneval_run_name=run_name)
            joined_record = json.loads((joined / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(joined_record["source_runs"], {"apps": parallel_name, "humaneval": run_name})
            self.assertEqual(joined_record["evaluation"]["apps"]["workers"], 4)
            self.assertEqual(joined_record["evaluation"]["humaneval"]["workers"], 1)


if __name__ == "__main__":
    unittest.main()
