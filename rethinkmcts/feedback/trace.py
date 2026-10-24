from __future__ import annotations

import ast
import base64
import json
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from Executors.common import run_python_file


@dataclass(frozen=True)
class TraceBlock:
    block_id: str
    line_start: int
    line_end: int
    source: str
    events: list[dict[str, object]]


@dataclass(frozen=True)
class TraceResult:
    status: str
    blocks: list[TraceBlock]
    error: str | None = None


def build_basic_blocks(source: str) -> list[tuple[str, int, int, str]]:
    """Build AST statement spans; this is not a complete control-flow graph."""
    tree = ast.parse(source)
    lines = source.splitlines()
    statements: list[ast.stmt] = [node for node in ast.walk(tree) if isinstance(node, ast.stmt)]
    statements.sort(key=lambda node: (getattr(node, "lineno", 0), getattr(node, "end_lineno", 0)))
    blocks: list[tuple[str, int, int, str]] = []
    seen: set[tuple[int, int]] = set()
    for index, node in enumerate(statements, start=1):
        start = getattr(node, "lineno", 1)
        end = getattr(node, "end_lineno", start)
        key = (start, end)
        if key in seen:
            continue
        seen.add(key)
        text = "\n".join(lines[start - 1 : end])
        blocks.append((f"BLOCK-{index}", start, end, text))
    return blocks


def _runner_source(source_b64: str, driver_b64: str, result_path: str, max_events: int) -> str:
    return f'''import base64
import json
import sys
import traceback

source = base64.b64decode({source_b64!r}).decode("utf-8")
driver = base64.b64decode({driver_b64!r}).decode("utf-8")
events = []

def snapshot(value):
    try:
        return repr(value)[:1000]
    except Exception:
        return "<unrepresentable>"

def trace(frame, event, arg):
    if (frame.f_code.co_filename in ("<candidate>", "<driver>")
            and event in ("line", "return", "exception") and len(events) < {max_events}):
        events.append({{
            "event": event,
            "file": frame.f_code.co_filename,
            "frame": id(frame),
            "line": frame.f_lineno,
            "locals": {{str(key): snapshot(value) for key, value in frame.f_locals.items()}},
        }})
    return trace

namespace = {{"__name__": "__candidate__"}}
status = "completed"
error = None
sys.settrace(trace)
try:
    exec(compile(source, "<candidate>", "exec"), namespace, namespace)
    exec(compile(driver, "<driver>", "exec"), namespace, namespace)
except BaseException:
    status = "runtime_error"
    error = traceback.format_exc()
finally:
    sys.settrace(None)
    with open({result_path!r}, "w", encoding="utf-8") as output:
        json.dump({{"status": status, "error": error, "events": events}}, output, ensure_ascii=False)
'''


def collect_trace(
    source: str,
    driver: str,
    *,
    stdin: str = "",
    timeout_seconds: float = 5.0,
    python_executable: str | Path | None = None,
    max_events: int = 2000,
) -> TraceResult:
    with tempfile.TemporaryDirectory(prefix="rethinkmcts-trace-") as temp_dir:
        root = Path(temp_dir)
        result_path = root / "trace.json"
        encoded_source = base64.b64encode(source.encode("utf-8")).decode("ascii")
        encoded_driver = base64.b64encode(driver.encode("utf-8")).decode("ascii")
        script = root / "trace_runner.py"
        script.write_text(
            _runner_source(encoded_source, encoded_driver, str(result_path), max_events),
            encoding="utf-8",
        )
        process = run_python_file(
            script,
            stdin=stdin,
            timeout_seconds=timeout_seconds,
            python_executable=python_executable or sys.executable,
        )
        if not result_path.is_file():
            return TraceResult(status=process.status, blocks=[], error=process.stderr or process.status)
        payload = json.loads(result_path.read_text(encoding="utf-8"))
        events = payload.get("events", [])[:max_events]
        try:
            static_blocks = build_basic_blocks(source)
        except SyntaxError as exc:
            return TraceResult(
                status="syntax_error",
                blocks=[],
                error=payload.get("error") or f"{type(exc).__name__}: {exc}",
            )
        block_events: dict[str, list[dict[str, object]]] = {}
        for index, event in enumerate(events):
            if event.get("file") != "<candidate>":
                continue
            line = int(event.get("line", 0))
            matching = [block for block in static_blocks if block[1] <= line <= block[2]]
            if not matching:
                continue
            block = min(matching, key=lambda item: (item[2] - item[1], item[1]))
            next_event = next(
                (later for later in events[index + 1 :] if later.get("frame") == event.get("frame")),
                None,
            )
            block_events.setdefault(block[0], []).append({
                "event": event.get("event"),
                "line": line,
                "before": event.get("locals", {}),
                "after": next_event.get("locals", {}) if next_event else None,
            })
        blocks = [
            TraceBlock(block_id, line_start, line_end, block_source, block_events[block_id])
            for block_id, line_start, line_end, block_source in static_blocks
            if block_id in block_events
        ]
        if not blocks:
            blocks = [
                TraceBlock(
                    block_id=f"BLOCK-{index + 1}",
                    line_start=int(event.get("line", 0)),
                    line_end=int(event.get("line", 0)),
                    source="",
                    events=[event],
                )
                for index, event in enumerate(events)
            ]
        return TraceResult(
            status=str(payload.get("status", process.status)),
            blocks=blocks,
            error=payload.get("error"),
        )


def format_trace(trace: TraceResult, *, max_blocks: int = 10, max_chars: int = 5000) -> str:
    blocks = trace.blocks[:max_blocks]
    if not blocks:
        return f"Trace status: {trace.status}\nError: {trace.error or 'no trace events'}"
    chunks: list[str] = [f"Trace status: {trace.status}"]
    for block in blocks:
        chunks.append(
            f"[{block.block_id}] lines {block.line_start}-{block.line_end}\n"
            + block.source[:max_chars]
            + "\n"
            + json.dumps(block.events, ensure_ascii=False)[:max_chars]
        )
    return "\n\n".join(chunks)
