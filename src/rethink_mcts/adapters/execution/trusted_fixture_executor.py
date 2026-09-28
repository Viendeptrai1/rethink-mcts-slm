"""
Trusted fixture subprocess executor implementing PublicExecutor port.
Used for unit/contract tests and development without requiring Docker daemon.
"""

import sys
import time
import subprocess
import tempfile
import os
import signal
from typing import List, Optional
from rethink_mcts.domain.candidate import (
    ProgramCandidate,
    SingleCaseResult,
    ExecutionSummary,
    CandidateVerdict
)
import json
from rethink_mcts.domain.problem import TestCase, StdinCase, FunctionCase, AssertionSuite, ExecutionSpec, ProblemLimits
from rethink_mcts.adapters.execution.comparators import get_comparator
from rethink_mcts.adapters.execution.harnesses import wrap_code_for_execution
from rethink_mcts.ports.execution import PublicExecutor


class TrustedFixtureExecutor(PublicExecutor):
    """
    Subprocess runner with syntax checking, output capping, timeout handling,
    and process cleanup.
    """
    def __init__(self, python_executable: str = sys.executable):
        self.python_executable = python_executable

    def evaluate(
        self,
        candidate: ProgramCandidate,
        tests: tuple[TestCase, ...],
        spec: ExecutionSpec,
        limits: ProblemLimits
    ) -> ExecutionSummary:
        if not tests:
            return ExecutionSummary.empty()

        # 1. Pre-execution Syntax Check (detect CE without running process)
        try:
            compile(candidate.code, "<candidate>", "exec")
        except SyntaxError as e:
            ce_res = SingleCaseResult(
                case_id=getattr(tests[0], "case_id", "c0"),
                status=CandidateVerdict.CE,
                error_message=f"SyntaxError at line {e.lineno}: {e.msg}"
            )
            return ExecutionSummary.create(total=len(tests), case_results=(ce_res,))

        case_results: List[SingleCaseResult] = []
        start_all = time.time()

        for test in tests:
            case_id = getattr(test, "case_id", f"case_{len(case_results)}")
            res = self._run_single_case(candidate.code, test, spec, limits, case_id)
            case_results.append(res)

        elapsed = time.time() - start_all
        return ExecutionSummary.create(
            total=len(tests),
            case_results=tuple(case_results),
            elapsed_seconds=elapsed
        )

    def _run_single_case(
        self,
        code: str,
        test_case: TestCase,
        spec: ExecutionSpec,
        limits: ProblemLimits,
        case_id: str
    ) -> SingleCaseResult:
        wrapped_code = wrap_code_for_execution(code, test_case, spec)
        stdin_input = ""
        expected_output = ""
        comparator_id = "token_text"

        if isinstance(test_case, StdinCase):
            stdin_input = test_case.stdin
            expected_output = test_case.expected_stdout
            comparator_id = test_case.comparator_id
        elif isinstance(test_case, FunctionCase):
            stdin_input = ""
            expected_output = json.dumps(test_case.expected)
            comparator_id = test_case.comparator_id

        # Write wrapped code to a temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write(wrapped_code)
            tmp_path = tmp.name

        start_time = time.time()
        timeout = limits.timeout_seconds
        stdout_cap = limits.stdout_limit_bytes

        try:
            process = subprocess.Popen(
                self._command(tmp_path, wrapped_code, limits),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True
            )

            try:
                stdout_data, stderr_data = process.communicate(
                    input=stdin_input,
                    timeout=timeout
                )
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                stdout_data, stderr_data = process.communicate()
                return SingleCaseResult(
                    case_id=case_id,
                    status=CandidateVerdict.TLE,
                    expected_output=expected_output,
                    error_message=f"Time limit of {timeout:.1f}s exceeded",
                    execution_time=timeout
                )

            elapsed = time.time() - start_time

            # Check Output Limit Exceeded (OLE)
            if len(stdout_data.encode("utf-8")) > stdout_cap:
                return SingleCaseResult(
                    case_id=case_id,
                    status=CandidateVerdict.OLE,
                    actual_output=stdout_data[:200] + "... [TRUNCATED]",
                    expected_output=expected_output,
                    error_message=f"Output exceeded limit of {stdout_cap} bytes",
                    execution_time=elapsed
                )

            # Check process exit code
            if isinstance(test_case, AssertionSuite):
                if process.returncode == 0:
                    return SingleCaseResult(
                        case_id=case_id,
                        status=CandidateVerdict.AC,
                        actual_output=stdout_data,
                        expected_output=expected_output,
                        execution_time=elapsed
                    )
                else:
                    err_msg = stderr_data.strip()
                    if self._is_infra_error(err_msg, process.returncode):
                        return SingleCaseResult(
                            case_id=case_id,
                            status=CandidateVerdict.INFRA_ERROR,
                            actual_output=stdout_data,
                            expected_output=expected_output,
                            error_message=err_msg,
                            execution_time=elapsed
                        )
                    status = CandidateVerdict.WA if "AssertionError" in err_msg else CandidateVerdict.RE
                    return SingleCaseResult(
                        case_id=case_id,
                        status=status,
                        actual_output=stdout_data,
                        expected_output=expected_output,
                        error_message=err_msg or f"Assertion suite failed with code {process.returncode}",
                        execution_time=elapsed
                    )

            # Check Runtime Error (RE) for non-assertion suite
            if process.returncode != 0:
                err_msg = stderr_data.strip()
                if self._is_infra_error(err_msg, process.returncode):
                    return SingleCaseResult(
                        case_id=case_id,
                        status=CandidateVerdict.INFRA_ERROR,
                        actual_output=stdout_data,
                        expected_output=expected_output,
                        error_message=err_msg,
                        execution_time=elapsed
                    )
                return SingleCaseResult(
                    case_id=case_id,
                    status=CandidateVerdict.RE,
                    actual_output=stdout_data,
                    expected_output=expected_output,
                    error_message=err_msg or f"Process exited with code {process.returncode}",
                    execution_time=elapsed
                )

            # Check Output Correctness with Comparator
            comparator = get_comparator(comparator_id)
            cmp_stdout = stdout_data.strip() if isinstance(test_case, FunctionCase) else stdout_data
            if comparator(cmp_stdout, expected_output):
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
            err_msg = str(e)
            status = CandidateVerdict.INFRA_ERROR if self._is_infra_error(err_msg, -1) else CandidateVerdict.RE
            return SingleCaseResult(
                case_id=case_id,
                status=status,
                expected_output=expected_output,
                error_message=err_msg,
                execution_time=time.time() - start_time
            )
        finally:
            self._cleanup()
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    @staticmethod
    def _is_infra_error(err_msg: str, returncode: int) -> bool:
        low = err_msg.lower()
        infra_indicators = (
            "docker.sock",
            "cannot connect to the docker daemon",
            "is the docker daemon running",
            "error during connect",
            "failed to create task for container",
            "failed to start container",
            "dial unix",
            "error response from daemon",
        )
        return any(ind in low for ind in infra_indicators)

    def _command(self, path, code, limits):
        return [self.python_executable, path]

    def _cleanup(self):
        pass
