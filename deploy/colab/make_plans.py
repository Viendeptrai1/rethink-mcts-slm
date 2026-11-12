#!/usr/bin/env python3
"""Write the plan files for the v3 Colab sessions (one model per session; the 7B model is split
over two sessions on the same GPU type). Each plan is executed by deploy/colab/run_plan.sh.

usage: python3 deploy/colab/make_plans.py <out-dir> [--workers 16]
"""
import argparse
import os
import shlex

E = 'http://127.0.0.1:8000/v1'
R = '/content/runs'
MODELS = {
    'qwen25c7b': dict(hf='Qwen/Qwen2.5-Coder-7B-Instruct', extra_body=None),
    'seedcoder8b': dict(hf='ByteDance-Seed/Seed-Coder-8B-Instruct', extra_body=None),
    'qwen35_9b': dict(hf='Qwen/Qwen3.5-9B', extra_body='{chat_template_kwargs: {enable_thinking: false}}'),
}
BON = ['--solver', 'best_of_n', '--samples-n', '16', '--set', 'sampling.code.temperature=0.8',
       '--set', 'sampling.code.top_p=0.95']


def model_args(short):
    m = MODELS[short]
    args = ['--set', f'model.base_url={E}', '--set', f"model.model={m['hf']}"]
    if m['extra_body']:
        args += ['--set', f"model.extra_body={m['extra_body']}"]
    return args


def run(name, config, workers, short, *extra):
    args = ['run', name, '--config', f'configs/v3_7b/{config}.yaml', '--output-dir', f'{R}/{name}',
            '--workers', str(workers), *extra, *model_args(short)]
    return ' '.join(shlex.quote(a) for a in args)


def serve(short):
    return f"serve {shlex.quote(MODELS[short]['hf'])} {short}"


def full_runs(short, workers, which=('apps_mcts', 'apps_bon16', 'apps_direct', 'he_mcts', 'he_bon16', 'he_direct')):
    table = {
        'apps_mcts': (f'v3_apps_{short}_mcts', 'apps_mcts', ()),
        'apps_bon16': (f'v3_apps_{short}_bon16', 'apps_baseline', BON),
        'apps_direct': (f'v3_apps_{short}_direct', 'apps_baseline', ('--solver', 'direct')),
        'he_mcts': (f'v3_humaneval_{short}_mcts', 'humaneval_mcts', ()),
        'he_bon16': (f'v3_humaneval_{short}_bon16', 'humaneval_baseline', BON),
        'he_direct': (f'v3_humaneval_{short}_direct', 'humaneval_baseline', ('--solver', 'direct')),
    }
    return [run(table[k][0], table[k][1], workers, short, *table[k][2]) for k in which]


def gate(short, workers):
    """Format and search-health check on problems outside the APPS cohort (and 3 HumanEval
    problems, used only to check the output format; nothing is tuned on them)."""
    names = [f'v3_gate_apps_{short}_mcts', f'v3_gate_apps_{short}_direct', f'v3_gate_humaneval_{short}_mcts']
    return [
        run(names[0], 'pilot_apps_mcts', min(workers, 5), short, '--limit', '5'),
        run(names[1], 'pilot_apps_baseline', min(workers, 5), short, '--solver', 'direct', '--limit', '5'),
        run(names[2], 'humaneval_mcts', 3, short, '--limit', '3'),
        'gate ' + ' '.join(f'{R}/{n}' for n in names),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--workers', type=int, default=16)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    w = a.workers
    plans = {
        'q7apps': [serve('qwen25c7b'), *full_runs('qwen25c7b', w, ('apps_mcts',))],
        'q7rest': [serve('qwen25c7b'), *full_runs('qwen25c7b', w, ('apps_bon16', 'apps_direct', 'he_mcts', 'he_bon16', 'he_direct'))],
        'seed': [serve('seedcoder8b'), *gate('seedcoder8b', w), *full_runs('seedcoder8b', w)],
        'qwen35': [serve('qwen35_9b'), *gate('qwen35_9b', w), *full_runs('qwen35_9b', w)],
    }
    for name, lines in plans.items():
        path = os.path.join(a.out, f'{name}.plan')
        with open(path, 'w') as f:
            f.write('\n'.join(lines) + '\n')
        print(path)


if __name__ == '__main__':
    main()
