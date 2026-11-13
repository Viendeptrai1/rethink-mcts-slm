#!/usr/bin/env python3
"""Protocol health and cost report for one or more run directories (reads runs/ only, no model calls).

For each run it reports what must hold before spending GPU on a full benchmark:
  - search shape: rollouts, evaluated nodes, maximum depth reached
  - feedback: share of block analyses that reached the feedback text (parsed or raw)
  - model output health: truncated generations (finish_reason=length), leaked <think> blocks,
    empty code, critic calls, errors
  - cost: input/output tokens and calls per problem and per role, model-side seconds
  - an "early stop" counterfactual: hidden verdict of the first candidate that passed all public tests
Optionally converts measured GPU time into a cost estimate for a full cohort.

Usage:
  python3 scripts/pilot_report.py runs/v3_apps_qwen25c7b_mcts [more runs...] \
      [--gpu-seconds 1234 --gpu-price-hour 1.95 --target-problems 300] [--json out.json]
"""
import argparse
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path


def load(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def depth_stats(search):
    if not search:
        return None, 0
    nodes = search['tree']['nodes']
    nodes = nodes.values() if isinstance(nodes, dict) else nodes
    # Backup copies the evaluation id up to the root, so the root is excluded.
    evaluated = [n for n in nodes if n.get('latest_evaluation_id') and n['node_id'] != search['tree']['root_id']]
    return (max((n['depth'] for n in evaluated), default=0), len(evaluated))


def analysis_reached_feedback(record):
    analysis = record['feedback'].get('analysis')
    if not analysis:
        return None  # no analysis requested/obtained for this feedback
    return bool(analysis.get('assessments') or analysis.get('summary_explanation') or analysis.get('raw_text'))


def problem_metrics(pdir):
    usage = load(pdir / 'usage.json', {})
    completed = load(pdir / 'completed.json')
    error = load(pdir / 'error.json')
    requests = load(pdir / 'requests.json', [])
    feedback = load(pdir / 'feedback.json', [])
    search = load(pdir / 'search.json')
    candidates = load(pdir / 'candidates.json', [])
    evaluations = load(pdir / 'evaluations.json', [])
    max_depth, evaluated_nodes = depth_stats(search)
    finish = Counter()
    think = 0
    model_seconds = 0.0
    for r in requests:
        resp = r.get('response') or {}
        finish[resp.get('finish_reason') or ('error' if r.get('error') else 'none')] += 1
        if '<think>' in (resp.get('content') or ''):
            think += 1
        model_seconds += resp.get('elapsed_seconds') or 0.0
    reached = [x for x in (analysis_reached_feedback(f) for f in feedback) if x is not None]
    # Early-stop counterfactual: first candidate (generation order) passing all public tests.
    by_id = {e['candidate_id']: e for e in evaluations}
    first_pass = next((c for c in sorted(candidates, key=lambda c: c.get('created_sequence', 0))
                       if by_id.get(c['candidate_id'], {}).get('execution_summary', {}).get('all_passed')), None)
    return dict(
        status=(completed or {}).get('status') or ('error' if error else 'missing'),
        hidden_pass=bool((completed or {}).get('all_hidden_passed')),
        rollouts=usage.get('rollouts'), code_generations=usage.get('code_generation_attempts'),
        rethinks=usage.get('rethink_attempts'), calls=usage.get('total_model_calls'),
        calls_by_role=usage.get('model_calls_by_role', {}), tokens_by_role=usage.get('tokens_by_role', {}),
        input_tokens=usage.get('input_tokens'), output_tokens=usage.get('output_tokens'),
        wall=usage.get('wall_time_seconds'), model_seconds=model_seconds,
        max_depth=max_depth, evaluated_nodes=evaluated_nodes, stop_reason=(search or {}).get('stop_reason'),
        analyses=len(reached), analyses_in_feedback=sum(reached), finish=finish, think_leaks=think,
        first_public_pass_id=first_pass['candidate_id'] if first_pass else None,
        selected_id=(load(pdir / 'selected.json', {}) or {}).get('candidate_id'),
    )


def summarize(run):
    run = Path(run)
    rows = {p.name: problem_metrics(p) for p in sorted((run / 'problems').glob('*')) if p.is_dir()}
    if not rows:
        return dict(run=str(run), problems=0)
    n = len(rows)
    vals = lambda k: [r[k] for r in rows.values() if r[k] is not None]
    mean = lambda k: round(statistics.mean(vals(k)), 2) if vals(k) else None
    finish = sum((r['finish'] for r in rows.values()), Counter())
    role_tokens = defaultdict(lambda: [0, 0])
    for r in rows.values():
        for role, t in r['tokens_by_role'].items():
            role_tokens[role][0] += t.get('input') or 0
            role_tokens[role][1] += t.get('output') or 0
    analyses = sum(r['analyses'] for r in rows.values())
    same_as_early_stop = sum(r['first_public_pass_id'] is not None and r['first_public_pass_id'] == r['selected_id']
                             for r in rows.values())
    with_public_pass = sum(r['first_public_pass_id'] is not None for r in rows.values())
    return dict(
        run=str(run), problems=n, status=dict(Counter(r['status'] for r in rows.values())),
        hidden_pass=sum(r['hidden_pass'] for r in rows.values()),
        mean_rollouts=mean('rollouts'), mean_code_generations=mean('code_generations'), mean_rethinks=mean('rethinks'),
        mean_calls=mean('calls'), mean_input_tokens=mean('input_tokens'), mean_output_tokens=mean('output_tokens'),
        mean_wall_seconds=mean('wall'), max_wall_seconds=max(vals('wall'), default=None),
        mean_model_seconds=mean('model_seconds'),
        max_depth_distribution=dict(sorted(Counter(r['max_depth'] for r in rows.values()).items(), key=lambda kv: str(kv[0]))),
        mean_evaluated_nodes=mean('evaluated_nodes'),
        stop_reasons=dict(Counter((r['stop_reason'] or '')[:40] for r in rows.values())),
        block_analyses=analyses,
        block_analysis_in_feedback_pct=round(100 * sum(r['analyses_in_feedback'] for r in rows.values()) / analyses, 1) if analyses else None,
        finish_reasons=dict(finish), think_leaks=sum(r['think_leaks'] for r in rows.values()),
        tokens_by_role={k: dict(input=v[0], output=v[1]) for k, v in sorted(role_tokens.items())},
        problems_with_public_pass=with_public_pass,
        selected_equals_first_public_pass=same_as_early_stop,
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('runs', nargs='+')
    ap.add_argument('--gpu-seconds', type=float, help='Billed GPU seconds for these runs (from modal billing report)')
    ap.add_argument('--gpu-price-hour', type=float, default=1.95, help='USD per GPU hour (Modal L40S = 1.95)')
    ap.add_argument('--target-problems', type=int, default=300)
    ap.add_argument('--json')
    args = ap.parse_args()
    reports = [summarize(r) for r in args.runs]
    for rep in reports:
        print(json.dumps(rep, indent=2, ensure_ascii=False))
    if args.gpu_seconds:
        measured = sum(r['problems'] for r in reports)
        per_problem = args.gpu_seconds / measured
        cost = per_problem * args.target_problems * args.gpu_price_hour / 3600
        print(f'GPU seconds per problem (all runs above together): {per_problem:.1f}; '
              f'estimated cost for {args.target_problems} problems: ${cost:.2f} at ${args.gpu_price_hour}/h')
    if args.json:
        Path(args.json).write_text(json.dumps(reports, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
