"""Tests for the v3 (paper-faithful) protocol: prompt variables, block-analysis parsing,
rollout budget, half public split and parallel benchmark workers."""
import json
from pathlib import Path

import pytest

from rethink_mcts.adapters.datasets.apps import parse_apps_record
from rethink_mcts.adapters.llm.http_gateway import HttpModelGateway
from rethink_mcts.adapters.llm.semantic import parse_block_analysis
from rethink_mcts.application.benchmark import run_benchmark
from rethink_mcts.bootstrap import create_solver
from rethink_mcts.config import AppConfig
from rethink_mcts.domain.errors import ConfigurationError
from rethink_mcts.domain.feedback import BlockVerdict, ExecutionFacts, TraceResult, VerbalFeedback
from rethink_mcts.domain.problem import ExecutionMode, ExecutionSpec, PublicProblem, StdinCase
from rethink_mcts.ports.models import GenerationResponse

WRONG_THOUGHT = "Check parity only: answer YES when w is even"


class RecordingGateway:
    """Returns a valid answer per role and records every prompt."""

    def __init__(self, analysis='{"blocks": [{"block": "bb_0", "correct": false, "explanation": "w=2 is wrong"}]}'):
        self.requests = []
        self.analysis = analysis

    def complete(self, request):
        self.requests.append(request)
        content = {
            'expansion': json.dumps({"thoughts": [{"thought": WRONG_THOUGHT, "reasonableness": 0.6},
                                                  {"thought": "Loop over all splits", "reasonableness": 0.4}]}),
            'code': 'w = int(input())\nprint("YES" if w % 2 == 0 else "NO")',
            'rethink': 'Require w > 2 as well as w even',
            'block_analysis': self.analysis,
            'critic': '{"evaluation": 0.5, "explanation": "ok"}',
        }[request.role]
        return GenerationResponse(content, 'stop', prompt_tokens=10, completion_tokens=5)

    def prompts(self, role):
        return [r.prompt for r in self.requests if r.role == role]


def watermelon():
    return PublicProblem('wm', 'Can w kilos be split into two positive even parts? Print YES or NO.',
                         ExecutionSpec(mode=ExecutionMode.STDIN),
                         (StdinCase('8\n', 'YES\n', case_id='p1'), StdinCase('2\n', 'NO\n', case_id='p2')))


def v3_config(**budget):
    config = AppConfig()
    config.prompts.bundle = 'native_v3'
    config.prompts.strict_variables = True
    config.search.width = 2
    config.search.max_rethinks_per_node = 1
    config.search.early_stop = 'none'
    config.reward.critic_score_min = -1.0
    config.reward.critic_score_max = 1.0
    config.budget.max_rollouts = budget.get('rollouts', 3)
    config.budget.max_code_generations = 64
    config.budget.max_search_iterations = 100
    config.budget.max_model_calls = 200
    config.budget.max_total_tokens = 10 ** 7
    return config


def v3_solver(tmp_path, gateway=None, **budget):
    solver, _ = create_solver(v3_config(**budget), run_dir=str(tmp_path))
    gateway = gateway or RecordingGateway()
    solver.generator.gateway = gateway
    return solver, gateway


def test_v3_templates_receive_every_variable_and_show_what_the_paper_shows(tmp_path):
    # strict_variables=True: a template referencing a variable the code does not pass raises.
    solver, gateway = v3_solver(tmp_path, rollouts=2)
    solver.solve(watermelon())

    rethink = gateway.prompts('rethink')
    # The first rollout evaluates the highest-prior thought; its rethink must show that thought.
    assert rethink and WRONG_THOUGHT in rethink[0]
    assert all('(most recent, to be replaced)' in p for p in rethink)
    analysis = gateway.prompts('block_analysis')
    assert analysis and all('Input:\n2' in p and 'Expected output:\nNO' in p for p in analysis)
    assert all('standard input/output' in p for p in gateway.prompts('expansion') + gateway.prompts('code'))
    assert not any('`None`' in r.prompt for r in gateway.requests)
    # The model's block analysis reaches the rethink prompt (it was always dropped in v2).
    assert all('w=2 is wrong' in p for p in rethink)


def test_v3_critic_prompt_uses_configured_range_and_thoughts(tmp_path):
    solver, gateway = v3_solver(tmp_path)
    solver.evaluator.critic.gateway = gateway
    score = solver.evaluator.critic.assess('statement', 'print(1)', active_thoughts=(WRONG_THOUGHT,))
    prompt = gateway.prompts('critic')[0]
    assert '[-1.0, 1.0]' in prompt and WRONG_THOUGHT in prompt
    assert score == 0.5


def test_unparsed_block_analysis_is_kept_verbatim_in_feedback(tmp_path):
    solver, gateway = v3_solver(tmp_path, gateway=RecordingGateway(analysis='Block bb_0 is wrong because w=2.'))
    result = solver.solve(watermelon())
    assert any('Block bb_0 is wrong because w=2.' in p for p in gateway.prompts('rethink'))
    levels = {r['feedback']['level'] for r in result.feedback_records}
    assert 'block' in levels


@pytest.mark.parametrize('content,expected', [
    ('{"block": "bb_1", "correct": false, "explanation": "off by one"}', [('bb_1', BlockVerdict.INCORRECT)]),
    ('{"blocks": [{"block": "bb_0", "correct": true}, {"block": "bb_1", "correct": "False"}]}',
     [('bb_0', BlockVerdict.CORRECT), ('bb_1', BlockVerdict.INCORRECT)]),
    ('[{"block_id": "bb_2", "verdict": "incorrect"}]', [('bb_2', BlockVerdict.INCORRECT)]),
    # The paper's example answer: several objects one after another, not a JSON list.
    ('{"block": "BLOCK-1", "correct": "True"}\n{"block": "BLOCK-2", "correct": "False"}',
     [('BLOCK-1', BlockVerdict.CORRECT), ('BLOCK-2', BlockVerdict.INCORRECT)]),
    ('```json\n{"block": "bb_0", "correct": false}\n```', [('bb_0', BlockVerdict.INCORRECT)]),
])
def test_block_analysis_parser_accepts_paper_and_prompt_formats(content, expected):
    assessments, _ = parse_block_analysis(content)
    assert [(a.block_id, a.verdict) for a in assessments] == expected


def test_block_analysis_parser_rejects_text_without_json():
    with pytest.raises(ValueError):
        parse_block_analysis('The second block is wrong.')


def test_feedback_text_includes_raw_analysis_when_nothing_parsed():
    from rethink_mcts.domain.feedback import BlockAnalysis
    feedback = VerbalFeedback('f', 'c', ExecutionFacts('WA', '2', 'NO', 'YES'), trace=TraceResult('success'),
                              analysis=BlockAnalysis('a', raw_text='free-form analysis'), level='block')
    assert 'free-form analysis' in feedback.format_as_text()


def test_rollout_budget_counts_initial_evaluations_not_rethink_regenerations(tmp_path):
    solver, gateway = v3_solver(tmp_path, rollouts=3)
    result = solver.solve(watermelon())
    usage = result.usage.to_dict()
    assert usage['rollouts'] == 3
    assert usage['rethink_attempts'] >= 1
    # Each failed rollout gets one rethink regeneration on top of its initial code.
    assert usage['code_generation_attempts'] == 3 + usage['rethink_attempts']
    assert 'Rollout limit' in result.stop_reason or result.stop_reason == 'budget_exhausted'


def test_without_rollout_limit_v1_code_generation_budget_still_binds(tmp_path):
    config = v3_config()
    config.budget.max_rollouts = None
    config.budget.max_code_generations = 4
    solver, _ = create_solver(config, run_dir=str(tmp_path))
    solver.generator.gateway = RecordingGateway()
    result = solver.solve(watermelon())
    assert result.usage.code_generation_attempts == 4


def apps_record(inputs, outputs, **extra):
    return dict(id=7, question='q', difficulty='interview',
                input_output=json.dumps(dict(inputs=inputs, outputs=outputs)), **extra)


def test_half_split_uses_floor_half_of_distinct_tests():
    pub, hid = parse_apps_record(apps_record(['1', '2', '3'], ['1', '2', '3']), 'half')
    assert len(pub.public_tests) == 1 and len(hid.hidden_suite.cases) == 2
    # Five distinct tests listed twice (like apps_4349): split the distinct ones, keep real hidden tests.
    inputs = ['a', 'b', 'c', 'd', 'e'] * 2
    pub, hid = parse_apps_record(apps_record(inputs, inputs), 'half')
    assert len(pub.public_tests) == 2 and len(hid.hidden_suite.cases) == 3
    public_inputs = {c.stdin for c in pub.public_tests}
    assert not public_inputs & {c.stdin for c in hid.hidden_suite.cases}


def test_first_two_split_is_unchanged_and_starter_code_is_kept():
    pub, hid = parse_apps_record(apps_record(['1', '2', '3', '4'], ['1', '2', '3', '4'], starter_code='class S:'))
    assert len(pub.public_tests) == 2 and len(hid.hidden_suite.cases) == 2
    assert pub.execution_spec.starter_code == 'class S:'
    with pytest.raises(ConfigurationError):
        parse_apps_record(apps_record(['1'], ['1']), 'half')


def test_gateway_merges_extra_body_into_payload(monkeypatch):
    sent = {}

    class Response:
        status_code = 200
        headers = {}

        def json(self):
            return {"choices": [{"message": {"content": "x"}, "finish_reason": "stop"}],
                    "usage": {"prompt_tokens": 1, "completion_tokens": 1}}

    def post(url, headers, json, timeout):
        sent.update(json)
        return Response()

    monkeypatch.setattr('requests.post', post)
    from rethink_mcts.ports.models import GenerationRequest
    gateway = HttpModelGateway('http://x/v1', 'm', extra_body={"chat_template_kwargs": {"enable_thinking": False}})
    gateway.complete(GenerationRequest('r', 'code', 'p'))
    assert sent['chat_template_kwargs'] == {"enable_thinking": False}


def multi_problem_config(tmp_path):
    pub = json.loads(Path('tests/fixtures/watermelon_public.json').read_text())
    hidden = json.loads(Path('tests/fixtures/watermelon_hidden.json').read_text())
    data = tmp_path / 'dataset'
    data.mkdir()
    lines = []
    for i in range(4):
        pid = f"{pub['problem_id']}_{i}"
        lines.append(json.dumps(dict(pub, problem_id=pid)))
        (data / f'{pid}.json').write_text(json.dumps(dict(hidden, problem_id=pid)))
    (data / 'public.jsonl').write_text('\n'.join(lines) + '\n')
    config = AppConfig.from_yaml_file('configs/smoke_mock.yaml')
    config.experiment.stage = 'smoke'
    config.data.prepared_public_path = str(data / 'public.jsonl')
    config.data.judge_suites_dir = str(data)
    return config


def test_parallel_workers_give_the_same_verdicts_as_sequential(tmp_path):
    config = multi_problem_config(tmp_path)
    sequential = run_benchmark(config, tmp_path / 'seq', workers=1)
    parallel = run_benchmark(config, tmp_path / 'par', workers=3)
    key = lambda s: [(r['problem_id'], r['status'], r.get('all_hidden_passed'), r.get('code_hash')) for r in s['results']]
    assert key(sequential) == key(parallel)
    assert parallel['processed_problems'] == 4
    # Resume after a parallel run loads every completed problem without solving again.
    assert key(run_benchmark(config, tmp_path / 'par', workers=3)) == key(parallel)


def test_v3_repair_and_call_based_prompts_render_strictly(tmp_path):
    solver, _ = create_solver(v3_config(), solver_type='iterative_repair', run_dir=str(tmp_path))
    gateway = RecordingGateway()
    solver.generator.gateway = gateway
    solver.solve(watermelon())
    assert gateway.prompts('code')
    model = solver.generator
    spec = ExecutionSpec(mode=ExecutionMode.ASSERTION_SUITE, entry_point='add')
    model.generate('Add two numbers', spec, ())
    assert 'Define `add`' in gateway.prompts('code')[-1]
