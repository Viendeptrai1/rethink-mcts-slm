"""Tests for the statistics and offline-reconstruction helpers of scripts/analyze_v3.py."""
import importlib.util
import json
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    'analyze_v3', Path(__file__).resolve().parents[2] / 'scripts' / 'analyze_v3.py')
A = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(A)


def test_wilson_matches_known_value():
    lo, hi = A.wilson(52, 300)  # qwen25c7b Direct APPS in the ledger: 17.3 [13.5-22.0]
    assert round(100 * lo, 1) == 13.5 and round(100 * hi, 1) == 22.0
    assert A.wilson(0, 0) == (0.0, 0.0)


def test_mcnemar_exact_counts_and_p():
    base = [True, False, False, False, True]
    meth = [True, True, True, False, False]
    w, l, p = A.mcnemar_exact(base, meth)
    assert (w, l) == (2, 1)
    assert p == pytest.approx(1.0)  # 2 * P(X <= 1 | n=3) = 2 * 4/8, capped at 1
    assert A.mcnemar_exact([True], [True]) == (0, 0, 1.0)
    w, l, p = A.mcnemar_exact([False] * 10, [True] * 10)
    assert (w, l) == (10, 0) and p == pytest.approx(2 / 2 ** 10)


def test_holm_is_monotone_and_capped():
    adj = A.holm([0.01, 0.04, 0.03])
    assert adj == pytest.approx([0.03, 0.06, 0.06])
    assert A.holm([0.9, 0.8]) == [1.0, 1.0]


def test_bootstrap_is_deterministic():
    a, b = [0, 1, 0, 1, 0, 0], [1, 1, 0, 1, 1, 0]
    assert A.bootstrap_diff(a, b, reps=500) == A.bootstrap_diff(a, b, reps=500)
    lo, hi = A.bootstrap_diff(a, b, reps=500)
    assert lo <= (sum(b) - sum(a)) / len(a) <= hi


def _req(role, finish='stop', pt=10, ct=5):
    return {'request': {'role': role}, 'response': {'finish_reason': finish, 'prompt_tokens': pt, 'completion_tokens': ct}}


def _cand(cid, seq, origin):
    return cid, {'candidate_id': cid, 'created_sequence': seq, 'origin': origin, 'code': '', 'code_hash': cid}


def test_request_timeline_rollouts_and_rethink(tmp_path):
    reqs = [
        _req('expansion'), _req('code'),                       # rollout 1 starts at 0
        _req('block_analysis'), _req('rethink'), _req('code'),  # rethink revision of rollout 1
        _req('code'), _req('critic'),                          # rollout 2 starts at 5 (no expansion)
        _req('expansion'), _req('code'),                       # rollout 3 starts at 7
        _req('rethink', finish='length'), _req('code'),        # truncated rethink: rollout 4 starts at 10
    ]
    (tmp_path / 'requests.json').write_text(json.dumps(reqs))
    cands = dict([_cand('a', 1, 'initial'), _cand('b', 2, 'rethink'), _cand('c', 3, 'initial'),
                  _cand('d', 4, 'initial'), _cand('e', 5, 'initial')])
    tok, cand_req, cand_roll, ends = A.request_timeline(tmp_path, cands)
    assert cand_req == {'a': 1, 'b': 4, 'c': 5, 'd': 8, 'e': 10}
    assert cand_roll == {'a': 1, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
    assert ends == {1: 5, 2: 7, 3: 10, 4: 11}
    assert len(tok) == len(reqs)


def test_request_timeline_rejects_misalignment(tmp_path):
    (tmp_path / 'requests.json').write_text(json.dumps([_req('code'), _req('code')]))
    with pytest.raises(ValueError):
        A.request_timeline(tmp_path, dict([_cand('a', 1, 'initial')]))
