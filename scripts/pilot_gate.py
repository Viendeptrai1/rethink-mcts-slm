#!/usr/bin/env python3
"""Pass/fail gate over pilot runs, using the pass criteria of configs/v3_7b/README.md.

Exit code 0 when every run passes, 1 otherwise; prints one line per check.
MCTS runs (detected by rollouts > 0) are also checked for search health.

  python3 scripts/pilot_gate.py runs/v3_gate_apps_seedcoder8b_mcts runs/v3_gate_apps_seedcoder8b_direct
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pilot_report import summarize  # noqa: E402


def checks(rep):
    n = rep['problems']
    calls = sum(rep['finish_reasons'].values()) or 1
    out = [
        ('problems present', n > 0, n),
        ('technical errors <= 5%', rep['status'].get('completed', 0) >= 0.95 * n, rep['status']),
        ('truncated outputs <= 5%', rep['finish_reasons'].get('length', 0) <= 0.05 * calls,
         f"{rep['finish_reasons'].get('length', 0)}/{calls}"),
        ('no <think> in outputs', rep['think_leaks'] == 0, rep['think_leaks']),
        ('no problem near the 3600 s cap', (rep['max_wall_seconds'] or 0) < 3500, rep['max_wall_seconds']),
    ]
    if 'expansion' in rep['tokens_by_role']:  # MCTS run
        depths = [int(d) for d in rep['max_depth_distribution'] if str(d).isdigit()]
        out += [
            ('16 rollouts per problem', (rep['mean_rollouts'] or 0) >= 15.5, rep['mean_rollouts']),
            ('block analysis reaches feedback >= 90%', (rep['block_analysis_in_feedback_pct'] or 0) >= 90
             or rep['block_analyses'] == 0, rep['block_analysis_in_feedback_pct']),
            ('some tree reaches depth >= 3', max(depths, default=0) >= 3, rep['max_depth_distribution']),
        ]
    return out


def main():
    ok = True
    for run in sys.argv[1:]:
        rep = summarize(run)
        for name, passed, value in checks(rep):
            ok &= bool(passed)
            print(f"{'PASS' if passed else 'FAIL'}  {run}: {name} ({value})")
    print('GATE_PASSED' if ok else 'GATE_FAILED')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
