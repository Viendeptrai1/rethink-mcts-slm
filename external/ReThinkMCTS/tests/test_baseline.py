import argparse
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from DataProcess import load_problem
from baselines.direct_generation import (
    build_user_prompt,
    extract_code,
    load_config,
    save_artifact,
)
from baselines.direct_generation.pipeline import is_complete_artifact
from baselines.direct_generation.cli import _evaluate_artifact, parse_args
from baselines.batch_generation import (
    GenerationOutcome,
    _completed_ids,
    _selected_ids,
    _single_command,
    main as batch_main,
    parse_args as parse_batch_args,
)
from Executors import ExecutionReport, TestCaseResult


class ProblemLoaderTests(unittest.TestCase):
    def test_load_apps_reads_only_problem_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            problem_dir = root / "apps" / "raw" / "test" / "0007"
            problem_dir.mkdir(parents=True)
            (problem_dir / "question.txt").write_text("Add two numbers.", encoding="utf-8")
            (problem_dir / "starter_code.py").write_text(
                "def add(a, b):\n    pass\n", encoding="utf-8"
            )
            (problem_dir / "solutions.json").write_text(
                '["do not read me"]', encoding="utf-8"
            )

            problem = load_problem("apps", "7", data_root=root)

            self.assertEqual(problem.problem_id, "0007")
            self.assertEqual(problem.statement, "Add two numbers.")
            self.assertIn("def add", problem.starter_code)

    def test_invalid_apps_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            load_problem("apps", "5000")


class PromptTests(unittest.TestCase):
    def test_apps_prompt_requests_complete_program(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            problem_dir = root / "apps" / "raw" / "test" / "0000"
            problem_dir.mkdir(parents=True)
            (problem_dir / "question.txt").write_text("Echo input.", encoding="utf-8")
            problem = load_problem("apps", "0", data_root=root)

        prompt = build_user_prompt(problem)
        self.assertIn("Echo input.", prompt)
        self.assertIn("complete program", prompt)

    def test_extract_code_prefers_fenced_code(self) -> None:
        response = "Explanation\n```python\nprint('ok')\n```"
        self.assertEqual(extract_code(response), "print('ok')")

    def test_extract_code_accepts_plain_source(self) -> None:
        self.assertEqual(extract_code("print('ok')\n"), "print('ok')")

    def test_save_artifact_writes_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            problem_dir = root / "data" / "apps" / "raw" / "test" / "0000"
            problem_dir.mkdir(parents=True)
            (problem_dir / "question.txt").write_text("Echo input.", encoding="utf-8")
            problem = load_problem("apps", "0", data_root=root / "data")

            run_dir = save_artifact(
                root / "outputs",
                run_name="test_run",
                model="org/model-name",
                problem=problem,
                user_prompt="prompt",
                raw_response="```python\nprint('ok')\n```",
                code="print('ok')",
                metadata={"evaluation": None},
            )

            self.assertEqual((run_dir / "solution.py").read_text(), "print('ok')\n")
            self.assertIn("test_run", str(run_dir))
            self.assertIn("org_model-name", str(run_dir))
            self.assertTrue((run_dir / "problem.txt").is_file())
            self.assertTrue((run_dir / "response.txt").is_file())
            self.assertTrue((run_dir / "metadata.json").is_file())

    def test_load_default_config(self) -> None:
        config_path = (
            Path(__file__).parents[1]
            / "baselines"
            / "direct_generation"
            / "configs"
            / "default.json"
        )
        config = load_config(config_path)
        self.assertIsNone(config.model)
        self.assertEqual(config.prompt_version, "v1")
        self.assertIsNone(config.max_tokens)

    def test_artifact_completeness_rejects_blank_or_truncated_code(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            solution = Path(temp_dir) / "solution.py"
            solution.write_text("\n", encoding="utf-8")
            self.assertFalse(
                is_complete_artifact({"finish_reason": "length"}, solution)
            )

            solution.write_text("print('partial')\n", encoding="utf-8")
            self.assertFalse(
                is_complete_artifact({"finish_reason": "length"}, solution)
            )
            self.assertTrue(is_complete_artifact({"finish_reason": "stop"}, solution))


class DatasetEntryPointTests(unittest.TestCase):
    def test_apps_entry_point_fixes_dataset(self) -> None:
        args = parse_args(
            ["--problem-id", "7", "--split", "train", "--dry-run"],
            dataset="apps",
        )

        self.assertEqual(args.dataset, "apps")
        self.assertEqual(args.split, "train")
        self.assertTrue(args.dry_run)

    def test_humaneval_entry_point_fixes_dataset(self) -> None:
        args = parse_args(["--problem-id", "0", "--dry-run"], dataset="humaneval")

        self.assertEqual(args.dataset, "humaneval")
        self.assertEqual(args.split, "test")
        self.assertIsNone(args.max_tests)

    def test_optional_evaluation_is_saved_beside_solution(self) -> None:
        report = ExecutionReport(
            dataset="apps",
            problem_id="0000",
            mode="stdin_stdout",
            status="passed",
            passed_tests=1,
            total_tests=1,
            available_tests=10,
            duration_seconds=0.01,
            tests=[
                TestCaseResult(
                    index=0,
                    status="passed",
                    passed=True,
                    duration_seconds=0.01,
                )
            ],
        )
        args = argparse.Namespace(
            dataset="apps",
            evaluation_timeout=None,
            problem_id="0",
            split="test",
            max_tests=1,
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("Executors.AppsExecutor") as executor_class:
                executor_class.return_value.evaluate.return_value = report
                actual, report_path = _evaluate_artifact(
                    args, "print('ok')", Path(temp_dir)
                )

            self.assertEqual(actual, report)
            self.assertTrue(report_path.is_file())
            self.assertIn('"passed_tests": 1', report_path.read_text(encoding="utf-8"))


class BatchEntryPointTests(unittest.TestCase):
    def test_limit_selects_first_ids_in_range(self) -> None:
        args = parse_batch_args(
            ["--start", "10", "--end", "20", "--limit", "3", "--plan"],
            dataset="apps",
        )

        self.assertEqual(_selected_ids(args), [10, 11, 12])

    def test_single_command_uses_dataset_wrapper_and_quiet_mode(self) -> None:
        args = parse_batch_args(
            ["--limit", "1", "--run-name", "test_batch", "--plan"],
            dataset="humaneval",
        )

        command = _single_command(args, dataset="humaneval", problem_id=7)

        self.assertIn("baselines.generate_humaneval", command)
        self.assertIn("--quiet", command)
        self.assertNotIn("--split", command)

    def test_resume_requires_evaluation_when_requested(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            args = parse_batch_args(
                [
                    "--limit",
                    "1",
                    "--run-name",
                    "resume_test",
                    "--output-dir",
                    temp_dir,
                    "--evaluate",
                    "--plan",
                ],
                dataset="apps",
            )
            artifact = (
                Path(temp_dir)
                / "direct_generation"
                / "resume_test"
                / "model"
                / "apps"
                / "0000_timestamp"
            )
            artifact.mkdir(parents=True)
            (artifact / "solution.py").write_text("print(0)\n", encoding="utf-8")
            (artifact / "response.txt").write_text("print(0)\n", encoding="utf-8")
            (artifact / "metadata.json").write_text(
                '{"requested_model":"org/model","generation_complete":true,"finish_reason":"stop","problem":{"dataset":"apps","problem_id":"0000"}}',
                encoding="utf-8",
            )

            self.assertEqual(
                _completed_ids(args, dataset="apps", target_model="org/model"), set()
            )
            (artifact / "evaluation.json").write_text("{}\n", encoding="utf-8")
            self.assertEqual(
                _completed_ids(args, dataset="apps", target_model="org/model"),
                {"0000"},
            )

    def test_generation_workers_run_requests_concurrently(self) -> None:
        active = 0
        maximum_active = 0
        lock = threading.Lock()

        def fake_run(args, *, dataset, position, problem_id):
            nonlocal active, maximum_active
            with lock:
                active += 1
                maximum_active = max(maximum_active, active)
            time.sleep(0.05)
            with lock:
                active -= 1
            result = subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout=f"Saved artifact: artifact-{problem_id}\n",
                stderr="",
            )
            return GenerationOutcome(position, problem_id, result)

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("baselines.batch_generation._run_problem", side_effect=fake_run):
                status = batch_main(
                    [
                        "--limit",
                        "4",
                        "--run-name",
                        "parallel_test",
                        "--model",
                        "org/model",
                        "--output-dir",
                        temp_dir,
                        "--generation-workers",
                        "2",
                    ],
                    dataset="apps",
                )

        self.assertEqual(status, 0)
        self.assertEqual(maximum_active, 2)


if __name__ == "__main__":
    unittest.main()
