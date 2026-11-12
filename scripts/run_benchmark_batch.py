"""Compatibility CLI for the versioned, dataset-independent benchmark runner."""
import argparse
from pathlib import Path
from rethink_mcts.application.benchmark import load_config, run_benchmark


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True)
    parser.add_argument('--dataset', help='Prepared dataset directory name (no hardcoded dataset list)')
    parser.add_argument('--solver', default='mcts', choices=['direct','best_of_n','mcts','iterative_repair','graph'])
    parser.add_argument('--samples-n', type=int, default=3)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--no-resume', action='store_true')
    parser.add_argument('--problem-ids')
    parser.add_argument('--difficulty')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--workers', type=int, default=1,
                        help='Problems solved concurrently in this process (keep below the CPU core count)')
    parser.add_argument('--set', dest='overrides', action='append', default=[])
    args = parser.parse_args()
    overrides = []
    if args.dataset:
        overrides.extend([f'data.adapter={args.dataset}',
                          f'data.prepared_public_path=prepared/{args.dataset}/public/problems.jsonl',
                          f'data.judge_suites_dir=prepared/{args.dataset}/judge/suites'])
    config = load_config(args.config, overrides + args.overrides)
    problem_ids = None
    if args.problem_ids:
        raw_val = args.problem_ids.strip()
        fpath = Path(raw_val[1:] if raw_val.startswith('@') else raw_val)
        if fpath.exists() and fpath.is_file():
            if fpath.suffix == '.json':
                import json
                jdata = json.loads(fpath.read_text())
                if 'problem_ids_csv' in jdata:
                    problem_ids = [x.strip() for x in jdata['problem_ids_csv'].split(',') if x.strip()]
                elif 'problem_ids' in jdata:
                    problem_ids = [str(x).strip() for x in jdata['problem_ids'] if str(x).strip()]
                elif isinstance(jdata, list):
                    problem_ids = [str(x).strip() for x in jdata if str(x).strip()]
            else:
                problem_ids = [line.strip() for line in fpath.read_text().splitlines() if line.strip() and not line.startswith('#')]
        else:
            problem_ids = [x.strip() for x in args.problem_ids.split(',') if x.strip()]

    result = run_benchmark(config, args.output_dir, args.solver, args.samples_n,
                          args.dry_run, not args.no_resume,
                          problem_ids,
                          args.difficulty, args.limit, workers=args.workers)
    if args.dry_run:
        print(f"Validated {len(result['manifest']['problem_ids'])} problems; no model calls or writes")
    else:
        print(f"Processed {result['processed_problems']}/{result['requested_problems']}; "
              f"passed {result['passed_problems']}; errors {result['error_problems']}")
        if result['error_problems']:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
