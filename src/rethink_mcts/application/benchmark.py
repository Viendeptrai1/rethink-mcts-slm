"""Dataset/model-independent benchmark runner with immutable protocol fingerprints.

Public problems are supplied to solvers. Hidden suites are loaded for judging
only after a selected program has been persisted. Resume is per problem, not
mid-search. A dry run performs local validation only and writes nothing.
"""
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path

from rethink_mcts.config import AppConfig
from rethink_mcts.adapters.datasets.jsonl import JSONLProblemSource, parse_case_dict
from rethink_mcts.domain.problem import HiddenProblem, HiddenSuite, JudgeSpec
from rethink_mcts.domain.candidate import ProgramCandidate, CandidateVerdict
from rethink_mcts.application.judge import HiddenJudge
from rethink_mcts.bootstrap import create_solver, create_executor


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    tmp.replace(path)


def load_config(path, overrides=()):
    import yaml
    data = AppConfig.from_yaml_file(str(path)).model_dump()
    for override in overrides:
        key, sep, value = override.partition('=')
        if not sep:
            raise ValueError('Override must be section.field=value')
        parts = key.split('.')
        node = data
        for part in parts[:-1]:
            if part not in node or not isinstance(node[part], dict):
                raise ValueError(f'Unknown override: {key}')
            node = node[part]
        if parts[-1] not in node:
            raise ValueError(f'Unknown override: {key}')
        node[parts[-1]] = yaml.safe_load(value)
    return AppConfig.model_validate(data)


def prepare_run(config, solver='mcts', samples_n=3, problem_ids=None, difficulty=None, limit=None):
    config = AppConfig.model_validate(config.model_dump())
    public_path = Path(config.data.prepared_public_path or f'prepared/{config.data.adapter}/public/problems.jsonl')
    hidden_dir = Path(config.data.judge_suites_dir or public_path.parent.parent / 'judge/suites')
    source = JSONLProblemSource(str(public_path))
    ids = list(source.list_problem_ids())
    if config.data.cohort_path:
        cohort = json.loads(Path(config.data.cohort_path).read_text())
        if isinstance(cohort, dict):
            cohort = (cohort['problem_ids'] if 'problem_ids' in cohort else
                      [x.strip() for x in cohort['problem_ids_csv'].split(',') if x.strip()])
        if len(cohort) != len(set(cohort)):
            raise ValueError('Duplicate problem IDs in cohort')
        missing = set(cohort) - set(ids)
        if missing:
            raise ValueError(f'Cohort IDs missing from public data: {sorted(missing)}')
        ids = list(cohort)
    if config.experiment.stage == 'test' and (problem_ids or difficulty or limit):
        raise ValueError('Final test cohort cannot be changed by ad hoc filters')
    if problem_ids:
        if set(problem_ids) - set(ids):
            raise ValueError('Requested problem IDs are absent from the cohort')
        ids = [p for p in ids if p in problem_ids]
    if difficulty:
        ids = [p for p in ids if source.get_problem(p).metadata.difficulty == difficulty]
    if limit:
        ids = ids[:limit]
    if not ids:
        raise ValueError('No eligible problems')
    if solver not in ('mcts', 'direct', 'best_of_n', 'iterative_repair', 'graph') or samples_n < 1:
        raise ValueError('Unsupported solver or invalid samples_n')
    problems, hidden_hashes = [], {}
    for pid in ids:
        if Path(pid).name != pid or pid in ('.', '..'):
            raise ValueError(f'Unsafe problem ID: {pid}')
        problem = source.get_problem(pid)
        if not problem.public_tests:
            raise ValueError(f'{pid} has no public tests; no silent exclusions')
        hidden_path = hidden_dir / f'{pid}.json'
        hidden_hashes[pid] = file_digest(hidden_path)
        # Validate suite availability/shape now; it never enters a solver input.
        hidden = json.loads(hidden_path.read_text())
        if hidden.get('problem_id') != pid or not hidden.get('hidden_suite', {}).get('cases'):
            raise ValueError(f'{pid}: missing or mismatched hidden suite')
        public_cases = {digest({k:v for k,v in asdict(c).items() if k != "case_id"}) for c in problem.public_tests}
        hidden_cases = {digest({k:v for k,v in asdict(parse_case_dict(c)).items() if k != 'case_id'}) for c in hidden['hidden_suite']['cases']}
        if public_cases & hidden_cases:
            raise ValueError(f'{pid}: exact public/hidden case overlap')
        problems.append(problem)
    repo = Path(__file__).resolve().parents[3]
    prompt_dir = repo / 'prompts' / config.prompts.bundle
    if not prompt_dir.is_dir():
        raise ValueError(f'Prompt bundle not found: {prompt_dir}')
    prompts = {str(p.relative_to(repo)): file_digest(p) for p in sorted(prompt_dir.glob('*.jinja'))}
    code = {str(p.relative_to(repo)): file_digest(p) for p in sorted((repo/'src/rethink_mcts').rglob('*.py'))}
    dependencies = {}
    for package in ('pydantic', 'jinja2', 'requests', 'pyyaml'):
        dependencies[package] = importlib.metadata.version(package)
    protocol = dict(schema_version=2, config=config.model_dump(), solver=solver, samples_n=samples_n,
                    problem_ids=ids, public_hash=file_digest(public_path), hidden_hashes=hidden_hashes,
                    prompt_hashes=prompts, source_hash=digest(code),
                    runtime=dict(python=platform.python_version(), platform=platform.platform(), packages=dependencies))
    manifest_id = digest(protocol)
    head = subprocess.run(['git','rev-parse','HEAD'], cwd=repo, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(['git','status','--porcelain'], cwd=repo, capture_output=True, text=True).stdout
    if not head and (repo/'GIT_COMMIT').exists():
        # Code shipped as `git archive` (e.g. to Colab) has no .git; the archive records its commit.
        head, dirty = (repo/'GIT_COMMIT').read_text().strip(), ''
    manifest = dict(protocol, manifest_id=manifest_id, git_revision=head, working_tree_dirty=bool(dirty))
    return problems, hidden_dir, manifest


def _persist_search(root, result, config):
    pdir = root / 'problems' / result.problem_id
    pdir.mkdir(parents=True, exist_ok=True)
    candidates, evaluations = [], []
    for candidate, evaluation in result.archive.entries:
        candidates.append(asdict(candidate))
        evaluations.append(asdict(evaluation))
    atomic_json(pdir/'candidates.json', candidates)
    atomic_json(pdir/'evaluations.json', evaluations)
    atomic_json(pdir/'usage.json', result.usage.to_dict())
    atomic_json(pdir/'search.json', dict(stop_reason=result.stop_reason,
                                      best_reward=result.best_reward, tree=asdict(result.tree)))
    if config.storage.save_raw_model_responses:
        atomic_json(pdir/'requests.json', list(result.request_records))
    if config.storage.save_trace:
        atomic_json(pdir/'feedback.json', list(result.feedback_records))
    if result.selected_candidate:
        c = result.selected_candidate
        atomic_json(pdir/'selected.json', dict(candidate_id=c.candidate_id, code_hash=c.code_hash))
        tmp = pdir/'selected.py.tmp'
        tmp.write_text(c.code)
        tmp.replace(pdir/'selected.py')
    return pdir


def _summary(root, manifest, results):
    n = len(manifest['problem_ids'])
    completed = [r for r in results if r['status'] == 'completed']
    successes = sum(r.get('all_hidden_passed', False) for r in results)
    observed_tokens = [r.get('usage', {}).get('total_tokens') for r in results]
    data = dict(schema_version=2, manifest_id=manifest['manifest_id'], requested_problems=n,
                processed_problems=len(results), completed_problems=len(completed),
                error_problems=sum(r['status']=='error' for r in results), passed_problems=successes,
                selected_solution_pass_at_1_percent=100*successes/n,
                completed_only_pass_at_1_percent=100*successes/len(completed) if completed else None,
                mean_hidden_pass_rate_completed=(sum(r['hidden_pass_rate'] for r in completed)/len(completed) if completed else None),
                total_model_calls=(sum(r['usage']['total_model_calls'] for r in results) if all('usage' in r for r in results) else None),
                total_tokens=sum(observed_tokens) if len(results)==n and all(v is not None for v in observed_tokens) else None,
                solve_wall_seconds=sum(r.get('solve_wall_seconds',0) for r in results),
                judge_wall_seconds=sum(r.get('judge_wall_seconds',0) for r in results), results=results)
    atomic_json(root/'summary.json', data)
    return data


def _load_completed(root, manifest, problem):
    marker = root/'problems'/problem.problem_id/'completed.json'
    if not marker.exists():
        return None
    record = json.loads(marker.read_text())
    selected = marker.parent/'selected.py'
    if record['manifest_id'] != manifest['manifest_id'] or (record.get('code_hash') and
            (not selected.exists() or ProgramCandidate.compute_hash(selected.read_text()) != record['code_hash'])):
        raise ValueError(f'Corrupted resume artifact: {problem.problem_id}')
    core = {k:v for k,v in record.items() if k != 'record_hash'}
    if digest(core) != record.get('record_hash'):
        raise ValueError(f'Corrupted completion marker: {problem.problem_id}')
    return record


def _run_problem(config, root, manifest, hidden_dir, problem, solver, samples_n):
    """Solve, persist and judge one problem. Self-contained, so it can run in a worker thread."""
    marker = root/'problems'/problem.problem_id/'completed.json'
    started = time.monotonic()
    record = dict(problem_id=problem.problem_id, manifest_id=manifest['manifest_id'], status='error')
    engine = None
    try:
        # A fresh solver (model adapter, executor, budget) per problem: no state is shared across threads.
        engine, _ = create_solver(config, solver, str(root), samples_n)
        result = engine.solve(problem)
        record['solve_wall_seconds'] = time.monotonic()-started
        pdir = _persist_search(root, result, config)
        record['usage'] = result.usage.to_dict()
        if result.selected_candidate is None:
            record.update(status='no_candidate', all_hidden_passed=False)
        else:
            # Only now open hidden test contents for judging the frozen selection.
            raw = json.loads((hidden_dir/f'{problem.problem_id}.json').read_text())
            suite = raw['hidden_suite']
            hidden = HiddenProblem(problem.problem_id,
                HiddenSuite(tuple(parse_case_dict(c) for c in suite['cases']),
                    suite.get('suite_id','hidden'), tuple(parse_case_dict(c) for c in suite.get('generated_cases',[]))),
                JudgeSpec(**raw.get('judge_spec',{})))
            judge_start = time.monotonic()
            judged = HiddenJudge(create_executor(config)).judge(result.selected_candidate, hidden,
                                                                 execution_spec=problem.execution_spec)
            if any(c.status == CandidateVerdict.INFRA_ERROR for c in judged.execution_summary.case_results):
                raise RuntimeError('Hidden judging infrastructure failure')
            atomic_json(pdir/'judge_results.json', asdict(judged))
            record.update(status='completed', code_hash=judged.code_hash,
                all_hidden_passed=judged.all_hidden_passed, hidden_pass_rate=judged.hidden_pass_rate,
                generated_pass_rate=(judged.generated_execution_summary.pass_rate if judged.generated_execution_summary else None),
                judge_wall_seconds=time.monotonic()-judge_start)
        record['record_hash'] = digest(record)
        atomic_json(marker, record)
    except Exception as exc:
        if engine is not None and hasattr(engine, 'last_budget'):
            engine.last_budget.update_wall_time()
            record['usage'] = engine.last_budget.usage.to_dict()
            if config.storage.save_raw_model_responses:
                atomic_json(root/'problems'/problem.problem_id/'requests.json', engine.last_budget.requests)
        record.update(error_type=type(exc).__name__, error=str(exc))
        atomic_json(root/'problems'/problem.problem_id/'error.json', record)
    return record


def run_benchmark(config, output_dir, solver='mcts', samples_n=3, dry_run=False,
                  resume=True, problem_ids=None, difficulty=None, limit=None, workers=1):
    """Run (or resume) a benchmark. workers > 1 solves that many problems concurrently in one
    process; each problem still has its own solver and output directory. Results do not depend
    on workers, but per-problem wall time can (shared CPU for test execution), so keep workers
    below the number of CPU cores and report it."""
    if workers < 1:
        raise ValueError('workers must be >= 1')
    problems, hidden_dir, manifest = prepare_run(config, solver, samples_n, problem_ids, difficulty, limit)
    if dry_run:
        return dict(dry_run=True, manifest=manifest)
    root = Path(output_dir)
    manifest_path = root/'manifest.json'
    if manifest_path.exists():
        old = json.loads(manifest_path.read_text())
        if old['manifest_id'] != manifest['manifest_id']:
            raise ValueError('Resume rejected: config/model/data/prompts/source/runtime changed; use a new run directory')
        if not resume:
            raise ValueError('Run already exists; choose a new directory instead of overwriting results')
    elif root.exists() and any(root.iterdir()):
        raise ValueError('Nonempty directory has no v2 manifest; legacy results are read-only')
    else:
        atomic_json(manifest_path, manifest)
    order = [p.problem_id for p in problems]
    done = {}
    lock = threading.Lock()

    def record_result(pid, record):
        with lock:
            done[pid] = record
            _summary(root, manifest, [done[i] for i in order if i in done])

    pending = []
    for problem in problems:
        record = _load_completed(root, manifest, problem)
        if record is not None:
            record_result(problem.problem_id, record)
        else:
            pending.append(problem)
    if workers == 1:
        for problem in pending:
            record_result(problem.problem_id,
                          _run_problem(config, root, manifest, hidden_dir, problem, solver, samples_n))
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(_run_problem, config, root, manifest, hidden_dir, p, solver, samples_n): p
                       for p in pending}
            for future in as_completed(futures):
                record_result(futures[future].problem_id, future.result())
    return _summary(root, manifest, [done[i] for i in order if i in done])
