#!/usr/bin/env python3
"""Offline "all tests" view of 14B APPS runs (no code execution, no model calls).

The 14B protocol judges the selected program only on the hidden suite (all tests
except the first two, which are public). The 7B branch judges on every test.
For the selected program both halves are already recorded:
  - public result: evaluations.json entry for the selected candidate_id
  - hidden result: judge_results.json
so the all-tests verdict is (public all passed AND hidden all passed) and the
all-tests pass rate is (public_passed + hidden_passed) / (public_total + hidden_total).

Writes runs/<run>/all_tests_offline.json for each run and prints a summary.
"""
import json
import sys
from collections import defaultdict
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ['benchmark_apps_14b_direct_300', 'benchmark_apps_14b_bon3_300', 'benchmark_apps_14b_dual_unified']
COHORT = ROOT / 'external/ReThinkMCTS/data/samples/benchmark_v2/apps_test_300.json'
LEVELS = ('introductory', 'interview', 'competition')


def load_difficulty():
    coh = json.loads(COHORT.read_text())
    return {f'apps_{k}': v for k, v in coh['difficulty_by_problem_id'].items()}


def per_problem(run):
    out = {}
    for pdir in sorted((ROOT / 'runs' / run / 'problems').iterdir()):
        jr_path = pdir / 'judge_results.json'
        if not jr_path.exists():
            continue
        jr = json.loads(jr_path.read_text())
        sel = json.loads((pdir / 'selected.json').read_text())
        evs = json.loads((pdir / 'evaluations.json').read_text())
        pub = next(e['execution_summary'] for e in evs if e['candidate_id'] == sel['candidate_id'])
        h_pass, h_tot = jr['hidden_passed'], jr['hidden_total']
        out[pdir.name] = dict(
            public_passed=pub['passed'], public_total=pub['total'], public_all=pub['all_passed'],
            hidden_passed=h_pass, hidden_total=h_tot, hidden_all=jr['all_hidden_passed'],
            hidden_rate=jr['hidden_pass_rate'],
            all_tests_pass=bool(pub['all_passed'] and jr['all_hidden_passed']),
            all_tests_rate=(pub['passed'] + h_pass) / (pub['total'] + h_tot),
        )
    return out


def mcnemar(a, b, ids):
    a_only = sum(1 for i in ids if a[i] and not b[i])
    b_only = sum(1 for i in ids if b[i] and not a[i])
    n = a_only + b_only
    chi2 = (abs(a_only - b_only) - 1) ** 2 / n if n else 0.0
    k = min(a_only, b_only)
    p_exact = min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n) if n else 1.0
    return dict(a_only=a_only, b_only=b_only, chi2_cc=round(chi2, 4), p_exact=p_exact)


def main():
    diff = load_difficulty()
    data = {run: per_problem(run) for run in RUNS}
    report = {}
    for run, rows in data.items():
        by = defaultdict(list)
        for pid, r in rows.items():
            by[diff[pid]].append(r)
        summ = {}
        for lv in LEVELS + ('overall',):
            rs = list(rows.values()) if lv == 'overall' else by.get(lv, [])
            if not rs:
                continue
            summ[lv] = dict(
                n=len(rs),
                hidden_pass=sum(r['hidden_all'] for r in rs),
                hidden_mean_rate=round(100 * sum(r['hidden_rate'] for r in rs) / len(rs), 2),
                all_tests_pass=sum(r['all_tests_pass'] for r in rs),
                all_tests_mean_rate=round(100 * sum(r['all_tests_rate'] for r in rs) / len(rs), 2),
                hidden_pass_but_public_fail=sum(r['hidden_all'] and not r['public_all'] for r in rs),
            )
        report[run] = summ
        (ROOT / 'runs' / run / 'all_tests_offline.json').write_text(
            json.dumps(dict(description=__doc__.strip().splitlines()[0], summary=summ, problems=rows),
                       indent=2, ensure_ascii=False), encoding='utf-8')
    D = {p: r['all_tests_pass'] for p, r in data['benchmark_apps_14b_direct_300'].items()}
    M = {p: r['all_tests_pass'] for p, r in data['benchmark_apps_14b_dual_unified'].items()}
    B = {p: r['all_tests_pass'] for p, r in data['benchmark_apps_14b_bon3_300'].items()}
    report['paired_all_tests'] = dict(
        mcts_vs_direct_300=mcnemar(M, D, sorted(D)),
        mcts_vs_bon3_160=mcnemar(M, B, sorted(B)),
        bon3_vs_direct_160=mcnemar(B, D, sorted(B)),
        subset160=dict(direct=sum(D[p] for p in B), bon3=sum(B.values()), mcts=sum(M[p] for p in B)),
    )
    json.dump(report, sys.stdout, indent=2)
    print()


if __name__ == '__main__':
    main()
