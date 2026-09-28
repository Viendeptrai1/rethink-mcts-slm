import json
from dataclasses import replace
from pathlib import Path

import pytest

from rethink_mcts.application.benchmark import run_benchmark, prepare_run, load_config
from rethink_mcts.bootstrap import create_solver
from rethink_mcts.config import AppConfig
from rethink_mcts.domain.budget import BudgetLimits, BudgetManager
from rethink_mcts.domain.candidate import ProgramCandidate
from rethink_mcts.domain.errors import BudgetExceededError, ConfigurationError
from rethink_mcts.domain.problem import PublicProblem, ExecutionSpec, StdinCase, FunctionCase, AssertionSuite, ProblemLimits
from rethink_mcts.ports.models import GenerationResponse
from rethink_mcts.adapters.execution.tracing import DynamicTraceCollector
from rethink_mcts.adapters.execution.trusted_fixture_executor import TrustedFixtureExecutor
from rethink_mcts.adapters.execution.docker_executor import DockerExecutor
from rethink_mcts.adapters.execution.harnesses import wrap_code_for_execution
from rethink_mcts.policies.feedback import FeedbackObservation, select_feedback


class Gateway:
    def __init__(self):
        self.requests = []

    def complete(self, request):
        self.requests.append(request)
        content = {
            'expansion': '{"thoughts":[{"text":"Print NO", "reasonableness":1}]}',
            'code': 'print("NO")',
            'rethink': 'Try a different strategy',
            'block_analysis': '{"assessments":[{"block_id":"bb_1","verdict":"incorrect","explanation":"Wrong output"}]}',
            'critic': '{"score":0.9}'
        }[request.role]
        return GenerationResponse(content, 'stop', prompt_tokens=10, completion_tokens=5)


def problem():
    return PublicProblem('tiny', 'Print YES', ExecutionSpec(),
                         (StdinCase('', 'YES', case_id='public'),))


def candidate(code):
    return ProgramCandidate('c', 'tiny', code, ProgramCandidate.compute_hash(code))


def model_solver(tmp_path, cap=10):
    config = AppConfig()
    config.budget.max_code_generations = 2
    config.budget.max_model_calls = cap
    config.search.width = 1
    config.sampling.code.temperature = 0.71
    config.sampling.code.top_p = 0.83
    config.sampling.code.max_output_tokens = 77
    config.experiment.seed = 13
    solver, _ = create_solver(config, run_dir=str(tmp_path))
    gateway = Gateway()
    solver.generator.gateway = gateway
    return solver, gateway


def test_real_request_accounting_includes_analyzer_and_effective_sampling(tmp_path):
    solver, gateway = model_solver(tmp_path)
    result = solver.solve(problem())
    assert [r.role for r in gateway.requests] == ['expansion','code','block_analysis','rethink','code']
    assert result.usage.total_model_calls == len(gateway.requests) == 5
    assert result.usage.to_dict()['total_tokens'] == 75
    assert result.usage.to_dict()['tokens_by_role']['block_analysis']['input'] == 10
    assert len(result.request_records) == 5
    assert all((r.temperature, r.top_p, r.max_output_tokens)==(0.71,0.83,77)
               for r in gateway.requests if r.role == 'code')
    assert [r.seed for r in gateway.requests] == list(range(13,18))


def test_reserve_refinement_calls_downgrades_analysis_at_call_cap(tmp_path):
    solver, gateway = model_solver(tmp_path, cap=4)
    result = solver.solve(problem())
    assert result.usage.total_model_calls == len(gateway.requests) == 4
    assert 'block_analysis' not in [r.role for r in gateway.requests]
    assert result.feedback_records[0]['feedback']['level'] == 'trace'


def test_missing_usage_is_null_and_model_budget_is_enforced():
    budget = BudgetManager(BudgetLimits(max_model_calls=1))
    budget.before_model_call('code')
    assert budget.usage.to_dict()['total_tokens'] is None
    with pytest.raises(BudgetExceededError):
        budget.before_model_call('critic')


@pytest.mark.parametrize('case', [FunctionCase('f', args=(2,), expected=3),
                                  AssertionSuite('assert f(2) == 3', entry_point='f')])
def test_trace_invokes_actual_function_harness(case):
    trace = DynamicTraceCollector().collect_trace(
        candidate('def f(x):\n    marker = x + 1\n    return marker'), case,
        ExecutionSpec(mode='function', entry_point='f'))
    assert trace.status == 'success'
    assert any(v.locals_after.get('marker') == '3' for v in trace.block_visits)
    assert any(v.locals_before.get('x') == '2' for v in trace.block_visits)


def test_trace_has_process_deadline_for_blocking_native_call():
    trace = DynamicTraceCollector().collect_trace(
        candidate('import time\ntime.sleep(10)'), StdinCase('', ''), ExecutionSpec(), timeout_seconds=.15)
    assert trace.status == 'timeout'


def test_timeout_does_not_fabricate_other_test_verdicts():
    code = 'import time\nx=input()\nif x == "slow": time.sleep(1)\nprint("OK")'
    result = TrustedFixtureExecutor().evaluate(candidate(code),
        (StdinCase('slow\n','OK',case_id='a'), StdinCase('fast\n','OK',case_id='b')),
        ExecutionSpec(), ProblemLimits(timeout_seconds=.15))
    assert [c.status.value for c in result.case_results] == ['TLE','AC']
    assert result.pass_rate == .5


def test_docker_command_receives_complete_harness_and_disables_fallback():
    executor = DockerExecutor()
    wrapped = wrap_code_for_execution('def f(): return 1', AssertionSuite('assert f() == 2'), ExecutionSpec())
    command = executor._command('unused', wrapped, ProblemLimits())
    assert command[-1] == wrapped and 'assert f() == 2' in command[-1]
    assert executor.allow_host_fallback is False


def test_feedback_selection_is_public_and_error_sensitive():
    wa = FeedbackObservation('WA', 0.5, 'hash1')
    assert select_feedback('adaptive', wa).level == 'trace'
    assert select_feedback('adaptive', wa, [wa]).level == 'block'
    improved = FeedbackObservation('WA', 0.75, 'hash2')
    assert select_feedback('adaptive', improved, [wa]).level == 'trace'
    for failure in ('CE','TLE'):
        obs = FeedbackObservation(failure, 0, 'same')
        assert select_feedback('adaptive', obs, [obs]*3).level == 'facts_only'


def test_none_feedback_sends_no_execution_facts(tmp_path):
    solver, gateway = model_solver(tmp_path)
    solver.feedback_service.mode = 'none'
    result = solver.solve(problem())
    rethink = next(r for r in gateway.requests if r.role == 'rethink')
    assert '[EXECUTION REPORT]' not in rethink.prompt
    assert '[EXECUTION TRACE' not in rethink.prompt
    assert not any(r.role == 'block_analysis' for r in gateway.requests)
    assert result.feedback_records[0]['feedback']['level'] == 'none'


def fixture_config(tmp_path):
    pub = json.loads(Path('tests/fixtures/watermelon_public.json').read_text())
    hidden = json.loads(Path('tests/fixtures/watermelon_hidden.json').read_text())
    data = tmp_path/'dataset'
    data.mkdir()
    (data/'public.jsonl').write_text(json.dumps(pub)+'\n')
    (data/f"{pub['problem_id']}.json").write_text(json.dumps(hidden))
    config = AppConfig.from_yaml_file('configs/smoke_mock.yaml')
    config.experiment.stage = 'smoke'
    config.data.prepared_public_path = str(data/'public.jsonl')
    config.data.judge_suites_dir = str(data)
    config.feedback.mode = 'adaptive'
    config.search.early_stop = 'public_all_passed'
    return config


def test_dry_run_never_calls_model_or_creates_output(tmp_path, monkeypatch):
    config = fixture_config(tmp_path)
    monkeypatch.setattr('requests.post', lambda *a, **k: pytest.fail('Network call'))
    config.model.transport = 'openai_compatible'
    config.experiment.allow_mock = False
    output = tmp_path/'dry'
    result = run_benchmark(config, output, dry_run=True)
    assert result['dry_run'] and not output.exists()


def test_complete_resume_is_immutable_and_costs_are_not_session_elapsed(tmp_path, monkeypatch):
    config = fixture_config(tmp_path)
    output = tmp_path/'run'
    first = run_benchmark(config, output)
    assert first['completed_problems'] == first['passed_problems'] == 1
    monkeypatch.setattr('rethink_mcts.application.benchmark.create_solver', lambda *a, **k: pytest.fail('Resumed solver'))
    second = run_benchmark(config, output)
    assert first == second
    assert second['total_tokens'] is None
    config.model.model = 'different-model'
    with pytest.raises(ValueError, match='Resume rejected'):
        run_benchmark(config, output)


def test_resume_rejects_selected_code_tampering(tmp_path):
    config = fixture_config(tmp_path)
    output = tmp_path/'run'
    run_benchmark(config, output)
    selected = next(output.glob('problems/*/selected.py'))
    selected.write_text('print("tampered")')
    with pytest.raises(ValueError, match='Corrupted resume'):
        run_benchmark(config, output)


@pytest.mark.parametrize('solver', ['direct','best_of_n','iterative_repair','graph'])
def test_all_baselines_use_same_prepared_dataset_interface(tmp_path, solver):
    config = fixture_config(tmp_path)
    report = run_benchmark(config, tmp_path/'run', solver=solver)
    assert report['processed_problems'] == 1
    assert report['error_problems'] == 0
    assert report['completed_problems'] == 1


def test_test_only_disables_critic_and_mean_backup_is_real(tmp_path):
    config = fixture_config(tmp_path)
    config.reward.policy = 'test_only'
    config.search.backup = 'mean'
    solver, _ = create_solver(config, run_dir=str(tmp_path/'run'))
    from rethink_mcts.policies.backup import MeanBackupPolicy
    assert isinstance(solver.backup_policy, MeanBackupPolicy)
    result = solver.solve(prepare_run(config)[0][0])
    assert result.usage.model_calls_by_role['critic'] == 0
    assert result.best_reward == 1


def test_apps_rejects_overlapping_split_and_mismatched_arrays():
    from rethink_mcts.adapters.datasets.apps import parse_apps_record
    for inputs, outputs in [(['1','2'],['1','2']), (['1','2','3'],['1'])]:
        with pytest.raises(ConfigurationError):
            parse_apps_record({'id':1,'question':'test','input_output':{'inputs':inputs,'outputs':outputs}})


def test_apps_removes_cross_split_duplicates_ignoring_case_ids():
    from rethink_mcts.adapters.datasets.apps import parse_apps_record
    public, hidden = parse_apps_record({'id':1, 'question':'Echo', 'input_output':{
        'inputs':['1','2','1','3'], 'outputs':['1','2','1','3']}})
    assert len(public.public_tests) == 2
    assert [c.stdin for c in hidden.hidden_suite.cases] == ['3\n']


def test_mean_backup_averages_rewards():
    from rethink_mcts.domain.tree import Tree, ThoughtProposal
    from rethink_mcts.policies.backup import MeanBackupPolicy
    tree = Tree.create_root('p')
    leaf = tree.create_child_node('root', ThoughtProposal('x',1,1), 'root')
    policy = MeanBackupPolicy()
    policy.backup(tree, leaf.node_id, 0.2, 'e1')
    policy.backup(tree, leaf.node_id, 0.8, 'e2')
    policy.backup(tree, leaf.node_id, 0.8, 'e2')
    assert tree.get_node('root').q_max == .5
    assert leaf.visits == 2


def test_expansion_receives_feedback_after_failed_revision(tmp_path):
    solver, gateway = model_solver(tmp_path)
    solver.budget_limits = replace(solver.budget_limits, max_code_generations=3,
                                  max_model_calls=20, max_search_iterations=10)
    result = solver.solve(problem())
    expansions = [r for r in gateway.requests if r.role == 'expansion']
    assert len(expansions) >= 2
    assert '[EXECUTION REPORT]' in expansions[1].prompt
    assert result.usage.total_model_calls == len(gateway.requests)


def test_exact_token_requirement_rejects_missing_provider_usage(tmp_path):
    solver, gateway = model_solver(tmp_path)
    solver.generator.require_exact_token_count = True
    gateway.complete = lambda r: GenerationResponse('print("YES")', 'stop')
    from rethink_mcts.domain.errors import ModelError
    with pytest.raises(ModelError, match='token usage'):
        solver.solve(problem())


def test_hidden_sentinel_never_reaches_requests_or_feedback(tmp_path, monkeypatch):
    config = fixture_config(tmp_path)
    config.model.transport = 'openai_compatible'
    config.experiment.allow_mock = False
    config.budget.max_code_generations = 2
    hidden_path = next(Path(config.data.judge_suites_dir).glob('*.json'))
    hidden = json.loads(hidden_path.read_text())
    hidden['hidden_suite']['cases'][0]['expected_stdout'] = 'HIDDEN_SENTINEL_DO_NOT_LEAK'
    hidden_path.write_text(json.dumps(hidden))
    fake = Gateway()
    monkeypatch.setattr('rethink_mcts.adapters.llm.http_gateway.HttpModelGateway.complete',
                        lambda self, request: fake.complete(request))
    output = tmp_path/'run'
    report = run_benchmark(config, output)
    assert report['completed_problems'] == 1
    for name in ('requests.json','feedback.json'):
        text = next(output.glob(f'problems/*/{name}')).read_text()
        assert 'HIDDEN_SENTINEL_DO_NOT_LEAK' not in text


def test_http_gateway_forwards_sampling_seed_and_usage_without_network(monkeypatch):
    from rethink_mcts.adapters.llm.http_gateway import HttpModelGateway
    from rethink_mcts.ports.models import GenerationRequest
    captured = {}
    class Response:
        status_code = 200
        def json(self):
            return {'choices':[{'message':{'content':'print(1)'},'finish_reason':'stop'}],
                    'usage':{'prompt_tokens':7,'completion_tokens':3}}
    def post(url, **kwargs):
        captured.update(kwargs)
        return Response()
    monkeypatch.setattr('requests.post', post)
    response = HttpModelGateway('http://offline/v1','fake').complete(
        GenerationRequest('r','code','prompt',temperature=.7,top_p=.8,max_output_tokens=12,seed=42))
    assert captured['json']['seed'] == 42
    assert captured['json']['temperature'] == .7
    assert response.prompt_tokens == 7 and response.completion_tokens == 3


def test_failed_provider_preserves_unknown_cost_and_error_status(tmp_path, monkeypatch):
    config = fixture_config(tmp_path)
    config.model.transport = 'openai_compatible'
    config.experiment.allow_mock = False
    def fail(self, request):
        raise RuntimeError('offline provider failure')
    monkeypatch.setattr('rethink_mcts.adapters.llm.http_gateway.HttpModelGateway.complete', fail)
    output = tmp_path/'run'
    report = run_benchmark(config, output)
    assert report['error_problems'] == 1
    assert report['completed_problems'] == 0
    assert report['total_model_calls'] == 1
    assert report['total_tokens'] is None
    assert not list(output.glob('problems/*/completed.json'))


def test_http_retry_failure_records_all_transport_attempts(monkeypatch):
    from rethink_mcts.adapters.llm.http_gateway import HttpModelGateway
    from rethink_mcts.application.model_calls import complete_request
    from rethink_mcts.domain.budget import BudgetManager, BudgetLimits
    from rethink_mcts.domain.errors import RateLimitedError
    from rethink_mcts.ports.models import GenerationRequest
    class Response:
        status_code = 429
        headers = {}
        text = 'rate limited'
    monkeypatch.setattr('requests.post', lambda *args, **kwargs: Response())
    monkeypatch.setattr('rethink_mcts.adapters.llm.http_gateway.time.sleep', lambda seconds: None)
    budget = BudgetManager(BudgetLimits())
    with pytest.raises(RateLimitedError):
        complete_request(HttpModelGateway('http://offline/v1', 'fake', max_retries=2),
                         GenerationRequest('r', 'code', 'prompt'), budget)
    assert budget.usage.total_model_calls == 1
    assert budget.usage.transport_attempts == 3
    assert budget.usage.to_dict()['total_tokens'] is None


def test_graph_requires_provider_usage_when_configured(tmp_path):
    from rethink_mcts.application.graph_solver import GraphSolver
    from rethink_mcts.domain.budget import BudgetLimits
    from rethink_mcts.domain.errors import ModelError
    gateway = Gateway()
    gateway.complete = lambda request: GenerationResponse('analysis', 'stop')
    solver = GraphSolver(gateway, None, BudgetLimits(), require_exact_token_count=True)
    with pytest.raises(ModelError, match='token usage'):
        solver.solve(problem())


def test_docker_real_container_execution_and_trace():
    import shutil
    if shutil.which("docker") is None:
        pytest.skip("Docker not installed")
    from rethink_mcts.adapters.execution.docker_executor import DockerExecutor
    from rethink_mcts.adapters.execution.tracing import DynamicTraceCollector
    executor = DockerExecutor(image="rethink-worker:py311", allow_host_fallback=False)
    cand = candidate("print('DOCKER_OK')")
    test_case = StdinCase("", "DOCKER_OK\n", case_id="c1")
    limits = ProblemLimits(timeout_seconds=5.0)
    summary = executor.evaluate(cand, [test_case], ExecutionSpec(mode="stdin"), limits)
    assert summary.all_passed is True
    assert summary.case_results[0].status.value == "AC"

    tracer = DynamicTraceCollector(backend="docker", image="rethink-worker:py311")
    tr_cand = candidate("a = 1\nb = a + 2\nprint(b)")
    trace_res = tracer.collect_trace(tr_cand, test_case, ExecutionSpec(mode="stdin"), timeout_seconds=5.0)
    assert trace_res.status == "success"
    assert len(trace_res.block_visits) > 0

