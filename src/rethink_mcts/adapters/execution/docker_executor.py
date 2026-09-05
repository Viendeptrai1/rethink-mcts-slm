"""
Docker worker sandbox executor implementing PublicExecutor port (§10.1).
"""

import subprocess
import time
import shutil
from typing import List, Optional
from rethink_mcts.domain.candidate import (
    ProgramCandidate,
    SingleCaseResult,
    ExecutionSummary,
    CandidateVerdict
)
from rethink_mcts.domain.problem import TestCase, StdinCase, FunctionCase, ExecutionSpec, ProblemLimits
from rethink_mcts.domain.errors import ExecutionError
from rethink_mcts.adapters.execution.comparators import get_comparator
from rethink_mcts.ports.execution import PublicExecutor


class DockerExecutor(PublicExecutor):
    """
    Executes candidate code inside an isolated, unprivileged Linux container:
    - network: none
    - read-only root
    - tmpfs workspace
    - cap-drop all
    - no-new-privileges
    - cpu, memory, pids limits
    """
    def __init__(
        self,
        image: str = "rethink-worker:py311",
        allow_host_fallback: bool = False
    ):
        self.image = image
        self.allow_host_fallback = allow_host_fallback
        self._docker_available = shutil.which("docker") is not None

    def evaluate(
        self,
        candidate: ProgramCandidate,
        tests: tuple[TestCase, ...],
        spec: ExecutionSpec,
        limits: ProblemLimits
    ) -> ExecutionSummary:
        if not tests:
            return ExecutionSummary.empty()

        # 1. Syntax check before container spawn
        try:
            compile(candidate.code, "<candidate>", "exec")
        except SyntaxError as e:
            ce_res = SingleCaseResult(
                case_id=getattr(tests[0], "case_id", "c0"),
                status=CandidateVerdict.CE,
                error_message=f"SyntaxError at line {e.lineno}: {e.msg}"
            )
            return ExecutionSummary.create(total=len(tests), case_results=(ce_res,))

        if not self._docker_available:
            if self.allow_host_fallback:
                from rethink_mcts.adapters.execution.trusted_fixture_executor import TrustedFixtureExecutor
                return TrustedFixtureExecutor().evaluate(candidate, tests, spec, limits)
            raise ExecutionError("Docker binary not found in PATH")

        case_results: List[SingleCaseResult] = []
        start_all = time.time()

        for test in tests:
            case_id = getattr(test, "case_id", f"case_{len(case_results)}")
            res = self._run_container_case(candidate.code, test, spec, limits, case_id)
            case_results.append(res)

        elapsed = time.time() - start_all
        return ExecutionSummary.create(
            total=len(tests),
            case_results=tuple(case_results),
            elapsed_seconds=elapsed
        )

    def _run_container_case(
        self,
        code: str,
        test_case: TestCase,
        spec: ExecutionSpec,
        limits: ProblemLimits,
        case_id: str
    ) -> SingleCaseResult:
        stdin_input = test_case.stdin if isinstance(test_case, StdinCase) else ""
        expected_output = test_case.expected_stdout if isinstance(test_case, StdinCase) else str(getattr(test_case, "expected", ""))
        comparator_id = getattr(test_case, "comparator_id", "token_text")

        timeout = limits.timeout_seconds
        mem_mb = limits.memory_mb
        stdout_cap = limits.stdout_limit_bytes

        # Command to pass script via stdin to python in container
        docker_cmd = [
            "docker", "run", "--rm", "-i",
            "--network", "none",
            "--read-only",
            "--tmpfs", "/workspace:rw,size=64m",
            "--user", "1000:1000",
            "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "-m", f"{mem_mb}m",
            "--pids-limit", "32",
            self.image,
            "python3", "-c", code
        ]

        start_time = time.time()
        try:
            process = subprocess.Popen(
                docker_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            try:
                stdout_data, stderr_data = process.communicate(
                    input=stdin_input,
                    timeout=timeout
                )
            except subprocess.TimeoutExpired:
                process.kill()
                stdout_data, stderr_data = process.communicate()
                return SingleCaseResult(
                    case_id=case_id,
                    status=CandidateVerdict.TLE,
                    expected_output=expected_output,
                    error_message=f"Timeout of {timeout:.1f}s exceeded in container",
                    execution_time=timeout
                )

            elapsed = time.time() - start_time

            if len(stdout_data.encode("utf-8")) > stdout_cap:
                return SingleCaseResult(
                    case_id=case_id,
                    status=CandidateVerdict.OLE,
                    actual_output=stdout_data[:200] + "... [TRUNCATED]",
                    expected_output=expected_output,
                    error_message=f"Output exceeded {stdout_cap} bytes",
                    execution_time=elapsed
                )

            if process.returncode != 0:
                err_msg = stderr_data.strip()
                status = CandidateVerdict.MLE if "MemoryError" in err_msg or process.returncode == 137 else CandidateVerdict.RE
                return SingleCaseResult(
                    case_id=case_id,
                    status=status,
                    actual_output=stdout_data,
                    expected_output=expected_output,
                    error_message=err_msg or f"Container process exited with code {process.returncode}",
                    execution_time=elapsed
                )

            comparator = get_comparator(comparator_id)
            if comparator(stdout_data, expected_output):
                return SingleCaseResult(
                    case_id=case_id,
                    status=CandidateVerdict.AC,
                    actual_output=stdout_data,
                    expected_output=expected_output,
                    execution_time=elapsed
                )
            else:
                return SingleCaseResult(
                    case_id=case_id,
                    status=CandidateVerdict.WA,
                    actual_output=stdout_data,
                    expected_output=expected_output,
                    error_message="Output mismatch",
                    execution_time=elapsed
                )

        except Exception as e:
            return SingleCaseResult(
                case_id=case_id,
                status=CandidateVerdict.INFRA_ERROR,
                expected_output=expected_output,
                error_message=f"Container execution error: {e}",
                execution_time=time.time() - start_time
            )
