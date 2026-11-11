#!/usr/bin/env python3
"""Paired analysis of the 14B runs on APPS-300 and HumanEval-164 (reads runs/ only, no model calls).

Combines the Nov 2026 extra runs (no-rethink MCTS, Iterative Repair, BoN-3 rest, HumanEval
Direct/BoN-3 on current code) with the original runs, and reports for each method:
  - hidden-suite verdict (14B protocol) and all-tests verdict (public + hidden, the 7B protocol)
  - per difficulty: n, passes, Pass@1 %, mean pass rate %
  - paired McNemar (exact p, chi2 with continuity correction) and paired bootstrap 95% CI
    of the Pass@1 difference, always on the problems BOTH methods completed
  - token / call usage per problem
Writes runs/analysis_extra_14b/summary.json and prints a compact report.
"""
import glob
import json
import os
import random
from collections import Counter
from math import comb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LEVELS = ('introductory', 'interview', 'competition')
DIFF = {f'apps_{k}': v for k, v in json.load(open(
    'external/ReThinkMCTS/data/samples/benchmark_v2/apps_test_300.json'))['difficulty_by_problem_id'].items()}

APPS = {
    'direct': ['benchmark_apps_14b_direct_300'],
    'bon3': ['benchmark_apps_14b_bon3_300', 'benchmark_apps_14b_bon3_rest140'],
    'mcts': ['benchmark_apps_14b_dual_unified'],
    'mcts_norethink': [f'benchmark_apps_14b_norethink_q{q}' for q in range(1, 5)],
    'iterative_repair': [f'benchmark_apps_14b_repair_q{q}' for q in range(1, 5)],
}
HUMANEVAL = {
    'direct': ['humaneval_direct_14b_v2'],
    'bon3': ['humaneval_bon3_14b_v2'],
    'mcts': ['humaneval_mcts_dual_14b'],
}
APPS_PAIRS = [('mcts', 'direct'), ('mcts', 'bon3'), ('mcts', 'mcts_norethink'), ('mcts', 'iterative_repair'),
              ('iterative_repair', 'direct'), ('mcts_norethink', 'direct'), ('bon3', 'direct')]
HE_PAIRS = [('mcts', 'direct'), ('mcts', 'bon3'), ('bon3', 'direct')]


def load_problem(pdir):
    jr = json.load(open(f'{pdir}/judge_results.json'))
    sel = json.load(open(f'{pdir}/selected.json'))
    evs = json.load(open(f'{pdir}/evaluations.json'))
    pub = next(e['execution_summary'] for e in evs if e['candidate_id'] == sel['candidate_id'])
    comp = json.load(open(f'{pdir}/completed.json'))
    u = comp['usage']
    return dict(
        hidden_pass=bool(jr['all_hidden_passed']), hidden_rate=jr['hidden_pass_rate'],
        all_pass=bool(pub['all_passed'] and jr['all_hidden_passed']),
        all_rate=(pub['passed'] + jr['hidden_passed']) / (pub['total'] + jr['hidden_total']),
        wall=comp['solve_wall_seconds'], tokens=u.get('total_tokens'), output_tokens=u.get('output_tokens'),
        calls=u.get('total_model_calls'), calls_by_role=u.get('model_calls_by_role', {}),
    )


def load_method(run_dirs):
    out = {}
    for run in run_dirs:
        for pdir in sorted(glob.glob(f'runs/{run}/problems/*')):
            if os.path.exists(f'{pdir}/completed.json') and os.path.exists(f'{pdir}/judge_results.json'):
                out[os.path.basename(pdir)] = load_problem(pdir)
    return out


def mcnemar(a, b, ids, key):
    a_only = sum(a[i][key] and not b[i][key] for i in ids)
    b_only = sum(b[i][key] and not a[i][key] for i in ids)
    n = a_only + b_only
    chi2 = (abs(a_only - b_only) - 1) ** 2 / n if n else 0.0
    k = min(a_only, b_only)
    p = min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n) if n else 1.0
    return dict(a_only=a_only, b_only=b_only, chi2_cc=round(chi2, 3), p_exact=float(f'{p:.3g}'))


def bootstrap(a, b, ids, key, reps=10000, seed=2027):
    rng = random.Random(seed)
    d = [int(a[i][key]) - int(b[i][key]) for i in ids]
    if not d:
        return None
    stats = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(reps))
    return dict(delta_pp=round(100 * sum(d) / len(d), 2),
                ci95_pp=[round(100 * stats[int(0.025 * reps)], 2), round(100 * stats[int(0.975 * reps) - 1], 2)])


def summarize(rows, levels):
    res = {}
    groups = [(lv, [r for p, r in rows.items() if DIFF.get(p) == lv]) for lv in levels] + [('overall', list(rows.values()))]
    for lv, rs in groups:
        if not rs:
            continue
        n = len(rs)
        res[lv] = dict(
            n=n,
            hidden_pass=sum(r['hidden_pass'] for r in rs), hidden_pass1=round(100 * sum(r['hidden_pass'] for r in rs) / n, 2),
            hidden_rate=round(100 * sum(r['hidden_rate'] for r in rs) / n, 2),
            all_pass=sum(r['all_pass'] for r in rs), all_pass1=round(100 * sum(r['all_pass'] for r in rs) / n, 2),
            all_rate=round(100 * sum(r['all_rate'] for r in rs) / n, 2),
            mean_tokens=round(sum(r['tokens'] or 0 for r in rs) / n), mean_calls=round(sum(r['calls'] or 0 for r in rs) / n, 2),
            wall_over_900s=sum(r['wall'] > 900 for r in rs),
        )
    return res


def paired(data, pairs, levels):
    out = {}
    for a, b in pairs:
        if a not in data or b not in data:
            continue
        common = sorted(set(data[a]) & set(data[b]))
        entry = dict(n_common=len(common))
        for key in ('hidden_pass', 'all_pass'):
            entry[key] = dict(overall=dict(**mcnemar(data[a], data[b], common, key), **(bootstrap(data[a], data[b], common, key) or {})))
            for lv in levels:
                ids = [p for p in common if DIFF.get(p) == lv]
                if ids:
                    entry[key][lv] = dict(n=len(ids), **mcnemar(data[a], data[b], ids, key))
        out[f'{a}_vs_{b}'] = entry
    return out


def main():
    apps = {m: load_method(r) for m, r in APPS.items()}
    he = {m: load_method(r) for m, r in HUMANEVAL.items()}
    report = dict(
        description=__doc__.strip().splitlines()[0],
        sources=dict(apps=APPS, humaneval=HUMANEVAL),
        apps=dict(coverage={m: len(v) for m, v in apps.items()},
                  per_method={m: summarize(v, LEVELS) for m, v in apps.items()},
                  paired=paired(apps, APPS_PAIRS, LEVELS),
                  calls_by_role={m: dict(sum((Counter(r['calls_by_role']) for r in v.values()), Counter())) for m, v in apps.items()}),
        humaneval=dict(coverage={m: len(v) for m, v in he.items()},
                       per_method={m: summarize(v, ()) for m, v in he.items()},
                       paired=paired(he, HE_PAIRS, ())),
    )
    os.makedirs('runs/analysis_extra_14b', exist_ok=True)
    json.dump(report, open('runs/analysis_extra_14b/summary.json', 'w'), indent=2, ensure_ascii=False)
    # Compact per-problem verdicts so the paired tests can be redone without the (gitignored) traces.
    keep = ('hidden_pass', 'hidden_rate', 'all_pass', 'all_rate', 'tokens', 'calls', 'wall')
    per_problem = {ds: {m: {p: {k: r[k] for k in keep} for p, r in sorted(rows.items())} for m, rows in data.items()}
                   for ds, data in (('apps', apps), ('humaneval', he))}
    json.dump(dict(difficulty=DIFF, **per_problem), open('runs/analysis_extra_14b/per_problem.json', 'w'),
              ensure_ascii=False)

    print('APPS (hidden / all-tests Pass@1 %, n)')
    for m, s in report['apps']['per_method'].items():
        cells = ' | '.join(f"{lv[:5]} {s[lv]['hidden_pass1']:.1f}/{s[lv]['all_pass1']:.1f} (n={s[lv]['n']})" for lv in (*LEVELS, 'overall') if lv in s)
        print(f'  {m:17s} {cells}')
    print('APPS paired (a vs b on common problems): hidden | all-tests')
    for k, v in report['apps']['paired'].items():
        h, a = v['hidden_pass']['overall'], v['all_pass']['overall']
        print(f"  {k:34s} n={v['n_common']:3d}  hid {h['a_only']}/{h['b_only']} p={h['p_exact']} d={h.get('delta_pp')} {h.get('ci95_pp')}"
              f" | all {a['a_only']}/{a['b_only']} p={a['p_exact']} d={a.get('delta_pp')} {a.get('ci95_pp')}")
    print('HumanEval Pass@1 %')
    for m, s in report['humaneval']['per_method'].items():
        if 'overall' in s:
            print(f"  {m:8s} {s['overall']['hidden_pass']}/{s['overall']['n']} = {s['overall']['hidden_pass1']:.2f}")
    for k, v in report['humaneval']['paired'].items():
        h = v['hidden_pass']['overall']
        print(f"  {k:16s} {h['a_only']}/{h['b_only']} p={h['p_exact']} d={h.get('delta_pp')} {h.get('ci95_pp')}")


if __name__ == '__main__':
    main()
