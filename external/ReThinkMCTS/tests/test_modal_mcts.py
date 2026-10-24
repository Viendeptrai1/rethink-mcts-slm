from __future__ import annotations

import os
import unittest
from unittest.mock import MagicMock, patch

from ChatModels.modal_gpu_client import ModalGpuClient
from tools.modal_mcts import run


class ModalGpuClientTests(unittest.TestCase):
    @patch("modal.Cls.from_name")
    def test_authenticated_function_response(self, from_name):
        remote = MagicMock(return_value={
            "content": "print(1)", "model": "qwen2.5-coder:7b-instruct",
            "finish_reason": "stop",
            "usage": {"prompt_tokens": 4, "completion_tokens": 3, "total_tokens": 7},
        })
        from_name.return_value.return_value.generate.remote = remote
        client = ModalGpuClient()
        result = client.generate(
            [{"role": "user", "content": "solve"}],
            model="qwen2.5-coder:7b-instruct", max_tokens=None,
            temperature=0.2, top_p=0.95,
        )
        self.assertEqual(result.content, "print(1)")
        self.assertEqual(result.usage["total_tokens"], 7)
        remote.assert_called_once()

    @patch("tools.modal_mcts.run.batch.main", return_value=0)
    def test_plan_never_looks_up_modal_function(self, batch_main):
        with patch.dict(os.environ, {}, clear=False), patch("modal.Cls.from_name") as from_name:
            self.assertEqual(run.main(["--plan"]), 0)
            from_name.assert_not_called()
            self.assertIn("--plan", batch_main.call_args.args[0])

    @patch("tools.modal_mcts.run.batch.main", return_value=0)
    def test_plan_forwards_selected_ids(self, batch_main):
        self.assertEqual(run.main([
            "--plan", "--dataset", "apps", "--problem-ids", "1684", "3702",
            "--apps-test-workers", "2",
        ]), 0)
        forwarded = batch_main.call_args.args[0]
        self.assertEqual(forwarded[forwarded.index("--problem-ids") + 1:][:2], ["1684", "3702"])
        self.assertEqual(forwarded[forwarded.index("--apps-test-workers") + 1], "2")

    @patch("tools.modal_mcts.run.batch.main", return_value=0)
    def test_plan_forwards_evaluator_and_pilot_manifest(self, batch_main):
        self.assertEqual(run.main([
            "--plan", "--dataset", "apps", "--evaluator-model", "qwen2.5-coder:14b-instruct",
            "--apps-sample-file", "data/samples/benchmark_v2/apps_test_30_external_evaluator_pilot.json",
        ]), 0)
        forwarded = batch_main.call_args.args[0]
        self.assertIn("--evaluator-model", forwarded)
        self.assertIn("--apps-sample-file", forwarded)

    @patch("tools.modal_mcts.run.batch.main", return_value=0)
    @patch("modal.Cls.from_name")
    def test_smoke_pins_digest_before_batch(self, from_name, batch_main):
        from_name.return_value.return_value.model_info.remote.return_value = {
            "model": "qwen2.5-coder:7b-instruct", "digest": "sha256:test",
            "models": {"qwen2.5-coder:7b-instruct": {"digest": "sha256:test"}},
            "gpu": "NVIDIA L40S", "ollama_version": "ollama 0.35.1",
        }
        with patch.dict(os.environ, {}, clear=False):
            self.assertEqual(run.main(["--smoke"]), 0)
            self.assertEqual(os.environ["OLLAMA_MODEL_DIGEST"], "sha256:test")
            self.assertIn("--smoke", batch_main.call_args.args[0])

    @patch("tools.modal_mcts.run.batch.main")
    @patch("modal.Cls.from_name")
    def test_preflight_checks_and_reports_both_models_without_search(self, from_name, batch_main):
        from_name.return_value.return_value.model_info.remote.return_value = {
            "model": "qwen2.5-coder:7b-instruct", "digest": "sha256:gen",
            "models": {
                "qwen2.5-coder:7b-instruct": {"digest": "sha256:gen"},
                "qwen2.5-coder:14b-instruct": {"digest": "sha256:eval"},
            },
            "gpu": "NVIDIA L40S", "ollama_version": "ollama 0.35.1",
        }
        with patch.dict(os.environ, {}, clear=False):
            self.assertEqual(run.main([
                "--preflight", "--evaluator-model", "qwen2.5-coder:14b-instruct",
            ]), 0)
            from_name.return_value.return_value.model_info.remote.assert_called_once_with(True)
            batch_main.assert_not_called()


if __name__ == "__main__":
    unittest.main()
