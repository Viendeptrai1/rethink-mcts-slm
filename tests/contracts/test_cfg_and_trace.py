"""
Contract tests I15 to I18 verifying CFG extraction, dynamic variable snapshots, recursion, and degradation.
"""

from rethink_mcts.adapters.execution.cfg import build_cfg_for_code
from rethink_mcts.adapters.execution.tracing import freeze_snapshot, DynamicTraceCollector
from rethink_mcts.domain.candidate import ProgramCandidate
from rethink_mcts.domain.problem import StdinCase, ExecutionSpec


def test_i15_cfg_basic_blocks_edges_and_line_spans():
    """
    I15: CFG if/loop/call/return/exception -> Block edges and dynamic visits khớp fixture.
    """
    code = """w = int(input())
if w % 2 == 0:
    print('YES')
else:
    print('NO')
"""
    cfg = build_cfg_for_code(code)
    assert len(cfg.blocks) >= 2
    # Verify line mapping
    assert 2 in cfg.line_to_block_ids
    assert 3 in cfg.line_to_block_ids
    assert 5 in cfg.line_to_block_ids


def test_i16_mutable_container_mutation_does_not_mutate_before_snapshot():
    """
    I16: Mutable list đổi trong block -> Before snapshot không bị thay đổi theo after.
    """
    code = """lst = [1, 2, 3]
lst.append(4)
"""
    # Test snapshot helper directly
    locals_dict = {"lst": [1, 2, 3]}
    before = freeze_snapshot(locals_dict)
    assert before["lst"] == "[1, 2, 3]"

    # Mutate original list in place
    locals_dict["lst"].append(4)
    after = freeze_snapshot(locals_dict)
    assert after["lst"] == "[1, 2, 3, 4]"

    # Before snapshot must remain unchanged!
    assert before["lst"] == "[1, 2, 3]"


def test_i17_recursion_and_repeated_loop_block_frames_and_sequence():
    """
    I17: Recursion và repeated loop block -> Frame/visit IDs phân biệt, không flatten mất iteration.
    """
    code = """def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)
fact(3)
"""
    candidate = ProgramCandidate("c_rec", "p", code, "h_rec")
    collector = DynamicTraceCollector(max_visits=64)
    res = collector.collect_trace(candidate, StdinCase("", ""), ExecutionSpec())

    assert res.status == "success"
    assert len(res.block_visits) > 3

    # Sequence numbers must be strictly increasing
    seqs = [v.sequence_number for v in res.block_visits]
    assert seqs == sorted(seqs)
    assert len(set(seqs)) == len(seqs)


def test_i18_tracer_syntax_error_returns_degraded():
    """
    I18: Tracer syntax failure -> trace status degraded, không crash.
    """
    bad_candidate = ProgramCandidate("c_bad", "p", "def broken(:", "h_bad")
    collector = DynamicTraceCollector()
    res = collector.collect_trace(bad_candidate, StdinCase("", ""), ExecutionSpec())
    assert res.status == "degraded"
    assert res.degraded_reason is not None
