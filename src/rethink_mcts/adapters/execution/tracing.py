"""
Dynamic bytecode and line tracer capturing BlockVisits and variable snapshots (§8.3, §8.4).
"""

import sys
import copy
import io
from typing import Any, Dict, List, Optional
from rethink_mcts.domain.candidate import ProgramCandidate
from rethink_mcts.domain.problem import TestCase, StdinCase, ExecutionSpec
from rethink_mcts.domain.feedback import BlockVisit, TraceResult
from rethink_mcts.adapters.execution.cfg import build_cfg_for_code, CodeCFG
from rethink_mcts.ports.execution import TraceCollector


def freeze_snapshot(
    locals_dict: Dict[str, Any],
    max_vars: int = 20,
    max_items: int = 10,
    max_chars: int = 160
) -> Dict[str, str]:
    """
    Freezes frame local variables into stringified primitive representations (§8.4).
    Guarantees that subsequent mutations in candidate code will NOT alter the snapshot (I16).
    """
    snapshot: Dict[str, str] = {}
    count = 0
    for k, v in locals_dict.items():
        if k.startswith("__"):
            continue
        if count >= max_vars:
            break

        try:
            # Handle standard containers with bounds
            if isinstance(v, (list, tuple, set)):
                items = list(v)[:max_items]
                repr_str = str(items)
                if len(v) > max_items:
                    repr_str = repr_str[:-1] + ", ...]"
            elif isinstance(v, dict):
                items = {str(dk): str(dv) for idx, (dk, dv) in enumerate(v.items()) if idx < max_items}
                repr_str = str(items)
                if len(v) > max_items:
                    repr_str = repr_str[:-1] + ", ...}"
            else:
                repr_str = repr(v)

            if len(repr_str) > max_chars:
                repr_str = repr_str[:max_chars] + "...[truncated]"

            snapshot[k] = repr_str
            count += 1
        except Exception:
            snapshot[k] = "<unserializable>"

    return snapshot


class _TraceLimitExceeded(Exception):
    pass


class DynamicTraceCollector(TraceCollector):
    """Trace the same harness in a disposable worker, never in the orchestrator.

    trusted_fixture is a host subprocess, NOT a security sandbox. Docker uses
    the same worker with read-only package mount and no network.
    """
    def __init__(self, max_visits=256, max_variables_per_frame=20, max_value_chars=160,
                 backend="trusted_fixture", image="rethink-worker:py311", max_container_items=10):
        self.max_visits = max_visits
        self.max_variables_per_frame = max_variables_per_frame
        self.max_value_chars = max_value_chars
        self.backend, self.image = backend, image
        self.max_container_items = max_container_items

    def collect_trace(self, candidate, failed_case, spec, timeout_seconds=5.0):
        import json
        import subprocess
        import os
        import signal
        import uuid
        from pathlib import Path
        from dataclasses import asdict
        from rethink_mcts.adapters.execution.harnesses import wrap_code_for_execution
        try:
            build_cfg_for_code(candidate.code)
        except (SyntaxError, ValueError) as exc:
            return TraceResult(status="degraded", degraded_reason=str(exc))
        payload = dict(code=candidate.code,
                       harness=wrap_code_for_execution(candidate.code, failed_case, spec),
                       stdin=failed_case.stdin if isinstance(failed_case, StdinCase) else "",
                       max_visits=self.max_visits, max_vars=self.max_variables_per_frame,
                       max_chars=self.max_value_chars, max_items=self.max_container_items)
        cmd = [sys.executable, "-m", "rethink_mcts.adapters.execution.trace_worker"]
        container_name = None
        env = os.environ.copy()
        package_root = str(Path(__file__).resolve().parents[3])
        env["PYTHONPATH"] = package_root
        if self.backend == "docker":
            container_name = "rethink-trace-" + uuid.uuid4().hex
            cmd = ["docker", "run", "--rm", "-i", "--name", container_name,
                   "--network", "none", "--read-only", "--cap-drop", "ALL",
                   "--security-opt", "no-new-privileges", "--user", "1000:1000",
                   "--memory", "512m", "--pids-limit", "32", "--cpus", "1",
                   "--env", "PYTHONPATH=/opt/rethink", "--env", "PYTHONDONTWRITEBYTECODE=1",
                   "--mount", f"type=bind,source={package_root},target=/opt/rethink,readonly",
                   self.image, "python3", "-m", "rethink_mcts.adapters.execution.trace_worker"]
        proc = None
        try:
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, env=env, start_new_session=True)
            stdout, stderr = proc.communicate(json.dumps(payload), timeout=max(0.001, timeout_seconds))
            if proc.returncode:
                return TraceResult(status="degraded", degraded_reason=stderr[-1000:] or f"Worker exit {proc.returncode}")
            data = json.loads(stdout)
            return TraceResult(status=data["status"],
                               block_visits=tuple(BlockVisit(**v) for v in data.get("block_visits", [])),
                               omitted_visits_count=data.get("omitted_visits_count", 0),
                               degraded_reason=data.get("degraded_reason"))
        except subprocess.TimeoutExpired:
            if proc:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.communicate()
            return TraceResult(status="timeout", degraded_reason="Trace worker deadline exceeded")
        except Exception as exc:
            return TraceResult(status="degraded", degraded_reason=str(exc))
        finally:
            if container_name:
                try:
                    subprocess.run(["docker", "rm", "-f", container_name], capture_output=True, timeout=5)
                except Exception:
                    pass
