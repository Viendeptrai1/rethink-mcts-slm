"""Docker execution uses the exact host harness/comparison protocol."""
import shutil
import subprocess
import uuid
import time
from rethink_mcts.adapters.execution.trusted_fixture_executor import TrustedFixtureExecutor
from rethink_mcts.domain.candidate import CandidateVerdict
from rethink_mcts.domain.errors import ExecutionError


class DockerExecutor(TrustedFixtureExecutor):
    def __init__(self, image="rethink-worker:py311", allow_host_fallback=False,
                 cpus=1.0, pids_limit=32):
        super().__init__()
        self.image = image
        self.allow_host_fallback = allow_host_fallback
        self.cpus, self.pids_limit = cpus, pids_limit
        self._container_name = None
        self._ready = False

    def evaluate(self, candidate, tests, spec, limits):
        if shutil.which("docker") is None:
            if self.allow_host_fallback:
                return TrustedFixtureExecutor().evaluate(candidate, tests, spec, limits)
            raise ExecutionError("Docker unavailable; host fallback is disabled")
        if not self._ready:
            try:
                probe = subprocess.run(["docker", "image", "inspect", self.image],
                                       capture_output=True, text=True, timeout=5)
            except (OSError, subprocess.TimeoutExpired) as exc:
                raise ExecutionError(f"Docker runtime unavailable: {exc}") from exc
            if probe.returncode:
                raise ExecutionError(f"Docker runtime/image unavailable: {probe.stderr[-500:]}")
            self._ready = True
        return super().evaluate(candidate, tests, spec, limits)

    def _run_single_case(self, code, test_case, spec, limits, case_id):
        max_retries = 2
        for attempt in range(max_retries + 1):
            res = super()._run_single_case(code, test_case, spec, limits, case_id)
            if res.status != CandidateVerdict.INFRA_ERROR or attempt == max_retries:
                return res
            # Sleep briefly to allow docker daemon socket/worker queue to recover
            time.sleep(0.5 * (attempt + 1))
        return res

    def _command(self, path, code, limits):
        self._container_name = "rethink-exec-" + uuid.uuid4().hex
        return ["docker", "run", "--rm", "-i", "--name", self._container_name,
                "--network", "none", "--read-only", "--tmpfs", "/tmp:rw,size=64m",
                "--user", "1000:1000", "--cap-drop", "ALL",
                "--security-opt", "no-new-privileges", "--memory", f"{limits.memory_mb}m",
                "--pids-limit", str(self.pids_limit), "--cpus", str(self.cpus),
                self.image, "python3", "-c", code]

    def _cleanup(self):
        if self._container_name:
            try:
                subprocess.run(["docker", "rm", "-f", self._container_name],
                               capture_output=True, timeout=5)
            except Exception:
                pass
            finally:
                self._container_name = None
