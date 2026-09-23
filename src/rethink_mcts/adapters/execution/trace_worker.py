"""JSON worker for bounded opcode traces. Candidate stdout is discarded."""
import io
import json
import sys
from dataclasses import asdict
from rethink_mcts.adapters.execution.cfg import build_cfg_for_code
from rethink_mcts.adapters.execution.tracing import freeze_snapshot
from rethink_mcts.domain.feedback import BlockVisit


class TraceLimit(Exception):
    pass


class Sink(io.TextIOBase):
    def write(self, text):
        return len(text)


def trace(payload):
    cfg = build_cfg_for_code(payload['code'])
    visits, frames = [], {}
    sequence, steps = 0, 0
    max_steps = 50000
    truncated = False

    def snapshot(frame):
        return freeze_snapshot(frame.f_locals, max_vars=payload['max_vars'],
                               max_items=payload['max_items'], max_chars=payload['max_chars'])

    def finish(frame, kind='fallthrough', exception=None):
        pending = frames.pop(id(frame), None)
        if pending is None:
            return
        block_id, before = pending
        block = cfg.blocks[block_id]
        if len(visits) >= payload['max_visits']:
            raise TraceLimit()
        visits.append(BlockVisit(
            visit_id=f'v_{len(visits)}', block_id=block_id, frame_id=str(id(frame)),
            sequence_number=len(visits), line_span=block.line_span,
            source_snippet=block.source_snippet, locals_before=before,
            locals_after=snapshot(frame), exit_kind=kind, exception_type=exception))

    def callback(frame, event, arg):
        nonlocal steps
        if frame.f_code.co_filename != '<candidate>':
            return None
        if event == 'call':
            frame.f_trace_opcodes = True
            frame.f_trace_lines = False
        steps += 1
        if steps > max_steps:
            raise TraceLimit()
        if event == 'opcode':
            key = (frame.f_code.co_qualname, frame.f_code.co_firstlineno, frame.f_lasti)
            block_id = cfg.offset_to_block_id.get(key)
            pending = frames.get(id(frame))
            # Starting the same block again is a distinct loop visit.
            if pending and (pending[0] != block_id or frame.f_lasti == cfg.blocks[pending[0]].start_offset):
                finish(frame, 'jump')
            if block_id and id(frame) not in frames:
                frames[id(frame)] = (block_id, snapshot(frame))
        elif event == 'exception':
            finish(frame, 'exception', arg[0].__name__)
        elif event == 'return':
            finish(frame, 'return')
        return callback

    # Compile user code and the appended harness separately. Code-object
    # identities/offsets stay identical to the CFG; test code is not traced.
    namespace = {'__name__': '__main__'}
    suffix = payload['harness'][len(payload['code']):]
    sys.stdin = io.StringIO(payload['stdin'])
    sys.stdout = sys.stderr = Sink()
    try:
        sys.settrace(callback)
        exec(compile(payload['code'], '<candidate>', 'exec'), namespace)
        if suffix.strip():
            exec(compile(suffix, '<test_harness>', 'exec'), namespace)
    except TraceLimit:
        truncated = True
    except BaseException:
        # Runtime failures are expected: their executed frames are the signal.
        pass
    finally:
        sys.settrace(None)
    return dict(status='success', block_visits=[asdict(v) for v in visits],
                omitted_visits_count=1 if truncated else 0)


def main():
    payload = json.load(sys.stdin)
    output = sys.stdout
    result = trace(payload)
    output.write(json.dumps(result))
    output.flush()


if __name__ == '__main__':
    main()
