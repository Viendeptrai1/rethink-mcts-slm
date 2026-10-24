from __future__ import annotations

import io
import json
import unittest
from unittest.mock import Mock, patch

from tools.gpu import run_generation


ARGS = [
    "--ssh-host", "gpu.example.test", "--ssh-port", "2797",
    "--dataset", "humaneval", "--run-name", "gpu_smoke", "--limit", "1",
]


class GpuGenerationTests(unittest.TestCase):
    def test_plan_does_not_open_tunnel_or_download(self) -> None:
        with patch.object(run_generation.subprocess, "run", return_value=Mock(returncode=0)) as run, \
             patch.object(run_generation.subprocess, "Popen") as tunnel:
            self.assertEqual(run_generation.main([*ARGS, "--plan"]), 0)
        tunnel.assert_not_called()
        self.assertIn("--plan", run.call_args.args[0])

    def test_existing_model_skips_pull_and_routes_requests_through_tunnel(self) -> None:
        process = Mock()
        with patch.object(run_generation, "_free_port", return_value=11435), \
             patch.object(run_generation, "_wait_for_server"), \
             patch.object(run_generation, "_models", return_value={run_generation.DEFAULT_MODEL}), \
             patch.object(run_generation, "_pull_model") as pull, \
             patch.object(run_generation.subprocess, "Popen", return_value=process) as tunnel, \
             patch.object(run_generation.subprocess, "run", return_value=Mock(returncode=0)) as run:
            self.assertEqual(run_generation.main(ARGS), 0)
        pull.assert_not_called()
        self.assertIn("127.0.0.1:11435:127.0.0.1:11434", tunnel.call_args.args[0])
        self.assertEqual(run.call_args.kwargs["env"]["LLM_BASE_URL"], "http://127.0.0.1:11435/v1")
        self.assertEqual(run.call_args.kwargs["env"]["LLM_PROVIDER"], "ollama")
        process.terminate.assert_called_once()

    def test_missing_model_is_pulled_before_generation(self) -> None:
        process = Mock()
        with patch.object(run_generation, "_free_port", return_value=11435), \
             patch.object(run_generation, "_wait_for_server"), \
             patch.object(run_generation, "_models", return_value=set()), \
             patch.object(run_generation, "_pull_model") as pull, \
             patch.object(run_generation.subprocess, "Popen", return_value=process), \
             patch.object(run_generation.subprocess, "run", return_value=Mock(returncode=0)):
            self.assertEqual(run_generation.main(ARGS), 0)
        pull.assert_called_once_with("http://127.0.0.1:11435", run_generation.DEFAULT_MODEL)

    def test_failed_pull_stops_generation_and_closes_tunnel(self) -> None:
        process = Mock()
        with patch.object(run_generation, "_free_port", return_value=11435), \
             patch.object(run_generation, "_wait_for_server"), \
             patch.object(run_generation, "_models", return_value=set()), \
             patch.object(run_generation, "_pull_model", side_effect=RuntimeError("pull failed")), \
             patch.object(run_generation.subprocess, "Popen", return_value=process), \
             patch.object(run_generation.subprocess, "run") as run:
            with self.assertRaisesRegex(RuntimeError, "pull failed"):
                run_generation.main(ARGS)
        run.assert_not_called()
        process.terminate.assert_called_once()

    def test_pull_requires_model_in_tags_after_success(self) -> None:
        response = io.BytesIO((json.dumps({"status": "success"}) + "\n").encode())
        with patch.object(run_generation, "urlopen", return_value=response), \
             patch.object(run_generation, "_models", return_value=set()):
            with self.assertRaisesRegex(RuntimeError, "still absent"):
                run_generation._pull_model("http://127.0.0.1:11435", run_generation.DEFAULT_MODEL)

    def test_full_generation_requires_explicit_confirmation(self) -> None:
        with self.assertRaises(SystemExit):
            run_generation.parse_args(ARGS[:-2])


if __name__ == "__main__":
    unittest.main()
