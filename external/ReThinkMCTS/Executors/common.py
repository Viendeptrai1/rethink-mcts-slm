from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


MAX_CAPTURE_CHARS = 16_000


@dataclass(frozen=True)
class ProcessResult:
    status: str
    returncode: int | None
    stdout: str
    stderr: str
    duration_seconds: float


@dataclass(frozen=True)
class TestCaseResult:
    index: int
    status: str
    passed: bool
    duration_seconds: float
    expected: Any = None
    actual: Any = None
    error: str | None = None


@dataclass(frozen=True)
class ExecutionReport:
    dataset: str
    problem_id: str
    mode: str
    status: str
    passed_tests: int
    total_tests: int
    available_tests: int
    duration_seconds: float
    tests: list[TestCaseResult] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        if self.total_tests == 0:
            return 0.0
        return self.passed_tests / self.total_tests

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["pass_rate"] = self.pass_rate
        return result

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


def clip_text(value: str, limit: int = 2_000) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + f"\n... <truncated {len(value) - limit} chars>"


def _read_capture(path: Path) -> str:
    data = path.read_bytes()
    text = data.decode("utf-8", errors="replace")
    return clip_text(text, MAX_CAPTURE_CHARS)


def _terminate_process_tree(process: subprocess.Popen[Any]) -> None:
    if process.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    if process.poll() is None:
        process.kill()
    process.wait()


def run_python_file(
    script_path: Path,
    *,
    stdin: str = "",
    timeout_seconds: float = 2.0,
    python_executable: str | Path = sys.executable,
) -> ProcessResult:
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")

    stdout_path = script_path.parent / ".executor-stdout"
    stderr_path = script_path.parent / ".executor-stderr"
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    started = time.perf_counter()
    with stdout_path.open("wb") as stdout_file, stderr_path.open("wb") as stderr_file:
        process = subprocess.Popen(
            [str(python_executable), "-I", "-u", str(script_path)],
            cwd=script_path.parent,
            stdin=subprocess.PIPE,
            stdout=stdout_file,
            stderr=stderr_file,
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONHASHSEED": "0"},
            text=True,
            start_new_session=os.name != "nt",
            creationflags=creationflags,
        )
        try:
            process.communicate(input=stdin, timeout=timeout_seconds)
            status = "completed"
        except subprocess.TimeoutExpired:
            _terminate_process_tree(process)
            status = "timeout"

    duration = time.perf_counter() - started
    return ProcessResult(
        status=status,
        returncode=process.returncode,
        stdout=_read_capture(stdout_path),
        stderr=_read_capture(stderr_path),
        duration_seconds=duration,
    )


def run_python_source(
    source: str,
    *,
    stdin: str = "",
    timeout_seconds: float = 2.0,
    python_executable: str | Path = sys.executable,
) -> ProcessResult:
    with tempfile.TemporaryDirectory(
        prefix="rethinkmcts-executor-", ignore_cleanup_errors=os.name == "nt"
    ) as temp_dir:
        script_path = Path(temp_dir) / "candidate.py"
        script_path.write_text(source, encoding="utf-8")
        return run_python_file(
            script_path,
            stdin=stdin,
            timeout_seconds=timeout_seconds,
            python_executable=python_executable,
        )


def build_report(
    *,
    dataset: str,
    problem_id: str,
    mode: str,
    available_tests: int,
    tests: list[TestCaseResult],
) -> ExecutionReport:
    passed = sum(test.passed for test in tests)
    return ExecutionReport(
        dataset=dataset,
        problem_id=problem_id,
        mode=mode,
        status="passed" if tests and passed == len(tests) else "failed",
        passed_tests=passed,
        total_tests=len(tests),
        available_tests=available_tests,
        duration_seconds=sum(test.duration_seconds for test in tests),
        tests=tests,
    )
