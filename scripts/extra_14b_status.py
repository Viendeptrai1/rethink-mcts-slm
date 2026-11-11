#!/usr/bin/env python3
"""One-line-per-run progress for the Nov 2026 extra 14B runs (reads runs/ only)."""
import glob, json, os, re, statistics, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
pat = sys.argv[1] if len(sys.argv) > 1 else 'runs/benchmark_apps_14b_*_q[1-4]'
dirs = sorted(glob.glob(pat)) + sorted(glob.glob('runs/benchmark_apps_14b_bon3_rest140')) + sorted(glob.glob('runs/humaneval_*_14b_v2'))
tot_done = 0
for d in dirs:
    m = os.path.join(d, 'manifest.json')
    n = len(json.load(open(m))['problem_ids']) if os.path.exists(m) else '?'
    comp = glob.glob(f'{d}/problems/*/completed.json')
    errs = glob.glob(f'{d}/problems/*/error.json')
    walls = [json.load(open(c))['solve_wall_seconds'] for c in comp]
    tot_done += len(comp)
    pidf = f"logs/extra_14b/{os.path.basename(d)}.pid"
    alive = '?'
    if os.path.exists(pidf):
        try: os.kill(int(open(pidf).read()), 0); alive = 'run'
        except OSError: alive = 'exit'
    s = f"{os.path.basename(d):38s} {len(comp):3d}/{n} err={len(errs)} {alive}"
    if walls:
        s += f" wall med={statistics.median(walls):.0f}s max={max(walls):.0f}s >900={sum(w>900 for w in walls)}"
    print(s)
g = open('logs/extra_14b/guard.log').read().strip().splitlines()[-1] if os.path.exists('logs/extra_14b/guard.log') else ''
mm = re.search(r'Credit Used=\\?\$([0-9.]+)', g)
print(f"TOTAL done={tot_done} | credit_used=${mm.group(1) if mm else '?'} | {time.strftime('%H:%M')}")
