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


class DynamicTraceCollector(TraceCollector):
    """
    Executes candidate code with tracing to record block visits and variable deltas.
    """
    def __init__(
        self,
        max_visits: int = 256,
        max_variables_per_frame: int = 20,
        max_value_chars: int = 160
    ):
        self.max_visits = max_visits
        self.max_variables_per_frame = max_variables_per_frame
        self.max_value_chars = max_value_chars

    def collect_trace(
        self,
        candidate: ProgramCandidate,
        failed_case: TestCase,
        spec: ExecutionSpec,
        timeout_seconds: float = 5.0
    ) -> TraceResult:
        try:
            cfg = build_cfg_for_code(candidate.code)
        except Exception as e:
            return TraceResult(status="degraded", degraded_reason=f"CFG extraction failed: {e}")

        stdin_content = failed_case.stdin if isinstance(failed_case, StdinCase) else ""
        visits: List[BlockVisit] = []
        omitted_count = 0
        seq_num = 0

        # State tracking during trace
        current_block_id: Optional[str] = None
        current_frame_id: Optional[int] = None
        current_locals_before: Dict[str, str] = {}
        current_line_span = (1, 1)

        def trace_fn(frame, event, arg):
            nonlocal seq_num, omitted_count, current_block_id, current_frame_id, current_locals_before, current_line_span
            if frame.f_code.co_filename != "<candidate>":
                return trace_fn

            line_no = frame.f_lineno
            matching_blocks = cfg.line_to_block_ids.get(line_no, [])
            block_id = matching_blocks[0] if matching_blocks else f"line_{line_no}"
            frame_id = id(frame)

            if event == "line":
                if block_id != current_block_id or frame_id != current_frame_id:
                    # Finalize previous block visit
                    if current_block_id is not None:
                        locals_after = freeze_snapshot(
                            frame.f_locals,
                            max_vars=self.max_variables_per_frame,
                            max_chars=self.max_value_chars
                        )
                        block_info = cfg.blocks.get(current_block_id)
                        snippet = block_info.source_snippet if block_info else ""

                        if len(visits) < self.max_visits:
                            visits.append(
                                BlockVisit(
                                    visit_id=f"v_{seq_num}",
                                    block_id=current_block_id,
                                    frame_id=str(current_frame_id),
                                    sequence_number=seq_num,
                                    line_span=current_line_span,
                                    source_snippet=snippet,
                                    locals_before=current_locals_before,
                                    locals_after=locals_after
                                )
                            )
                        else:
                            omitted_count += 1

                    # Start new block visit
                    seq_num += 1
                    current_block_id = block_id
                    current_frame_id = frame_id
                    current_locals_before = freeze_snapshot(
                        frame.f_locals,
                        max_vars=self.max_variables_per_frame,
                        max_chars=self.max_value_chars
                    )
                    b_info = cfg.blocks.get(block_id)
                    current_line_span = b_info.line_span if b_info else (line_no, line_no)

            elif event == "return":
                if current_block_id is not None:
                    locals_after = freeze_snapshot(
                        frame.f_locals,
                        max_vars=self.max_variables_per_frame,
                        max_chars=self.max_value_chars
                    )
                    b_info = cfg.blocks.get(current_block_id)
                    snippet = b_info.source_snippet if b_info else ""
                    if len(visits) < self.max_visits:
                        visits.append(
                            BlockVisit(
                                visit_id=f"v_{seq_num}",
                                block_id=current_block_id,
                                frame_id=str(id(frame)),
                                sequence_number=seq_num,
                                line_span=current_line_span,
                                source_snippet=snippet,
                                locals_before=current_locals_before,
                                locals_after=locals_after,
                                exit_kind="return"
                            )
                        )
                    else:
                        omitted_count += 1
                current_block_id = None

            return trace_fn

        # Run traced execution in controlled namespace
        orig_stdin = sys.stdin
        orig_stdout = sys.stdout
        orig_stderr = sys.stderr

        sys.stdin = io.StringIO(stdin_content)
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        compiled_code = compile(candidate.code, "<candidate>", "exec")
        sandbox_globals = {"__name__": "__main__"}

        try:
            sys.settrace(trace_fn)
            exec(compiled_code, sandbox_globals)
        except Exception:
            # Test cases can raise expected exceptions during tracing
            pass
        finally:
            sys.settrace(None)
            sys.stdin = orig_stdin
            sys.stdout = orig_stdout
            sys.stderr = orig_stderr

        return TraceResult(
            status="success",
            block_visits=tuple(visits),
            omitted_visits_count=omitted_count
        )
