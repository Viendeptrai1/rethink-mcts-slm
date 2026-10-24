from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from pydantic import ValidationError

from Executors.common import ExecutionReport, TestCaseResult
from rethinkmcts.config import SearchConfig
from rethinkmcts.feedback.trace import collect_trace, format_trace
from rethinkmcts.parsing import parse_score, parse_thoughts
from rethinkmcts.policies import p_ucb_score, select_child
from rethinkmcts.prompts import code_prompt, feedback_prompt
from rethinkmcts.reward import compute_reward
from rethinkmcts.runner import ArtifactWriter, DatasetSearchExecutor, LLMOperations, load_context
from rethinkmcts.search import ProblemContext, SearchEngine, SearchResult
from rethinkmcts.tree import CandidateRecord, SearchNode
from rethinkmcts.workflow import WorkflowState, build_search_graph


def report(*, passed: bool, dataset: str = "apps") -> ExecutionReport:
    status = "passed" if passed else "failed"
    test = TestCaseResult(
        index=0,
        status=status if passed else "wrong_answer",
        passed=passed,
        duration_seconds=0.01,
        expected="ok",
        actual="ok" if passed else "bad",
        error=None if passed else "wrong answer",
    )
    return ExecutionReport(
        dataset=dataset,
        problem_id="0000" if dataset == "apps" else "HumanEval/0",
        mode="fake",
        status=status,
        passed_tests=int(passed),
        total_tests=1,
        available_tests=1,
        duration_seconds=0.01,
        tests=[test],
    )


class FakeLLM:
    def __init__(self) -> None:
        self.generated = 0

    def expand_thoughts(self, context, node, width):
        from rethinkmcts.parsing import ThoughtProposal

        return [ThoughtProposal(thought="Use a direct algorithm.", reasonableness=1.0)]

    def generate_code(self, context, node):
        self.generated += 1
        return "bad" if self.generated == 1 else "good"

    def self_evaluate(self, context, node, code):
        return 0.5

    def analyze_feedback(self, context, node, code, failed_test, trace_text):
        return json.dumps({"block": "BLOCK-1", "correct": False, "explanation": "bad"})

    def rethink(self, context, node, code, feedback):
        return "Handle the failing edge case explicitly."


class FakeExecutor:
    def __init__(self):
        self.final_calls = 0

    def evaluate_public(self, context, code):
        return report(passed=code == "good")

    def evaluate_private(self, context, code):
        return report(passed=True)

    def evaluate_final(self, context, code):
        self.final_calls += 1
        return report(passed=True)

    def trace_failure(self, context, code, failed_test_index):
        return "[BLOCK-1] x=bad"


class RethinkMCTSTests(unittest.TestCase):
    def test_external_evaluator_is_used_only_for_self_evaluation(self):
        calls = []

        class RoutingClient:
            def generate(self, messages, **kwargs):
                calls.append(kwargs["model"])
                return SimpleNamespace(content='{"evaluation": 0.5}', model=kwargs["model"],
                                       finish_reason="stop", usage={})

        operations = LLMOperations(
            RoutingClient(),
            SearchConfig(model="generator-7b", evaluator_model="judge-14b"),
        )
        operations._call("expand", "prompt")
        operations._call("self_evaluation", "prompt")
        self.assertEqual(calls, ["generator-7b", "judge-14b"])
        self.assertEqual([item.model for item in operations.calls], calls)

    def test_evaluator_model_requires_dual_and_must_be_distinct(self):
        with self.assertRaisesRegex(ValueError, "only valid"):
            SearchConfig(model="generator", evaluator_model="judge", reward_mode="test_only").validate()
        with self.assertRaisesRegex(ValueError, "must differ"):
            SearchConfig(model="same", evaluator_model="same").validate()

    def test_p_ucb_uses_q_and_prior_without_forcing_unvisited(self):
        parent = SearchNode("root", visit_count=10)
        low = SearchNode("low", parent=parent, prior=0.2, visit_count=2, q_value=0.8)
        high = SearchNode("high", parent=parent, prior=0.05, visit_count=0, q_value=0.0)
        parent.children = [low, high]

        self.assertEqual(select_child(parent), low)
        self.assertGreater(p_ucb_score(parent, low), 0.8)
        high.prior = 0.9
        self.assertEqual(select_child(parent), high)

    def test_test_only_reward_skips_llm_self_evaluation(self):
        class NoSelfEvaluationLLM(FakeLLM):
            def self_evaluate(self, context, node, code):
                raise AssertionError("test_only must not call self_evaluate")

        context = ProblemContext("apps", "test", "0000", "Print ok.", public_test_count=1)
        result = SearchEngine(context, NoSelfEvaluationLLM(), FakeExecutor(),
                              SearchConfig(rollouts=1, width=1, max_rethink_times=1,
                                           reward_mode="test_only")).run()
        self.assertEqual([candidate.reward for candidate in result.candidates], [0.0, 1.0])
        self.assertTrue(all(candidate.llm_score is None for candidate in result.candidates))
        self.assertEqual(result.best_candidate.reward, 1.0)

    def test_external_evaluator_is_not_called_when_public_tests_fail(self):
        class NoEvaluationOnFailure(FakeLLM):
            def __init__(self):
                super().__init__()
                self.evaluations = 0

            def generate_code(self, context, node):
                return "bad"

            def self_evaluate(self, context, node, code):
                self.evaluations += 1
                raise AssertionError("public-test failure must skip v_llm")

        llm = NoEvaluationOnFailure()
        SearchEngine(
            ProblemContext("apps", "test", "0000", "Print ok.", public_test_count=1),
            llm, FakeExecutor(),
            SearchConfig(rollouts=1, width=1, max_rethink_times=0, model="generator",
                         evaluator_model="external-evaluator"),
        ).run()
        self.assertEqual(llm.evaluations, 0)

    def test_invalid_reward_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            SearchConfig(reward_mode="unknown").validate()

    def test_parse_thoughts_normalizes_scores_and_accepts_paper_keys(self):
        proposals = parse_thoughts(
            "```json\n[{\"Thought-1\": \"A\", \"Reasonableness\": 2}, "
            "{\"thought\": \"B\", \"reasonableness\": 1}]\n```",
            width=2,
        )
        self.assertEqual([proposal.thought for proposal in proposals], ["A", "B"])
        self.assertAlmostEqual(sum(proposal.reasonableness for proposal in proposals), 1.0)

    def test_pydantic_contracts_reject_invalid_graph_state_and_thought(self):
        from rethinkmcts.parsing import ThoughtProposal

        with self.assertRaises(ValidationError):
            WorkflowState(root="not a tree")
        with self.assertRaises(ValidationError):
            WorkflowState(root=SearchNode("root"), rollout=-1)
        with self.assertRaises(ValidationError):
            ThoughtProposal(thought="", reasonableness=1.0)
        with self.assertRaises(ValidationError):
            ThoughtProposal(thought="valid", reasonableness=2.0)

    def test_parse_score_clips_to_paper_range(self):
        self.assertEqual(parse_score('{"evaluation": 4}'), 1.0)
        self.assertEqual(parse_score('{"evaluation": -4}'), -1.0)

    def test_parser_rejects_malformed_thought_output(self):
        with self.assertRaises(ValueError):
            parse_thoughts("not json", width=3)
        with self.assertRaises(ValueError):
            parse_thoughts('[{"thought": "Only one", "reasonableness": 1}]', width=2)
        with self.assertRaises(ValueError):
            parse_thoughts('[{"thought": "Same", "reasonableness": 0.5}, {"thought": "same", "reasonableness": 0.5}]', width=2)
        with self.assertRaises(ValueError):
            parse_thoughts('[{"thought": "A", "reasonableness": NaN}]', width=1)

    def test_dual_evaluation_reward(self):
        self.assertEqual(compute_reward(0.5), 0.5)
        self.assertAlmostEqual(compute_reward(1.0, 1.0), 1.0)
        self.assertAlmostEqual(compute_reward(1.0, -1.0), 0.6)

    def test_apps_context_splits_first_half_as_public(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_root = Path(temp_dir) / "data"
            problem_dir = data_root / "apps" / "raw" / "test" / "0000"
            problem_dir.mkdir(parents=True)
            (problem_dir / "question.txt").write_text("Echo input.", encoding="utf-8")
            (problem_dir / "input_output.json").write_text(
                json.dumps({"inputs": ["a", "b", "c", "d"], "outputs": ["a", "b", "c", "d"]}),
                encoding="utf-8",
            )
            context = load_context("apps", 0, data_root=data_root)
            self.assertEqual(context.public_test_count, 2)
            self.assertEqual(context.to_dict()["public_policy"], "half")
            self.assertEqual(context.private_test_indices, (2, 3))

    def test_sparse_apps_split_can_keep_two_public_tests(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_root = Path(temp_dir) / "data"
            problem_dir = data_root / "apps" / "raw" / "test" / "0000"
            problem_dir.mkdir(parents=True)
            (problem_dir / "question.txt").write_text("Echo input.", encoding="utf-8")
            (problem_dir / "input_output.json").write_text(
                json.dumps({"inputs": ["a", "b", "c"], "outputs": ["a", "b", "c"]}),
                encoding="utf-8",
            )
            original = load_context("apps", 0, data_root=data_root)
            adjusted = load_context("apps", 0, data_root=data_root, public_cases_type="half_min2")
            self.assertEqual((original.public_test_count, original.private_test_indices), (1, (1, 2)))
            self.assertEqual((adjusted.public_test_count, adjusted.private_test_indices), (2, (2,)))
            self.assertEqual(adjusted.to_dict()["public_policy"], "half_min2")

    def test_apps_prompts_distinguish_standard_input_from_call_based(self):
        standard = code_prompt("Echo the value.", ["Read one line."], dataset="apps")
        called = code_prompt("Add values.", ["Add arguments."], dataset="apps", function_name="add")
        self.assertIn("Read from stdin", standard)
        self.assertIn("print the answer to stdout", standard)
        self.assertIn("call-based", called)
        self.assertIn("`add`", called)
        self.assertIn("Return the result instead of printing", called)
        feedback = feedback_prompt("Echo.", [], "def solve(): pass", "actual: empty", "trace",
                                   dataset="apps")
        self.assertIn("stdout is empty", feedback)
        self.assertIn("missing driver", feedback)

    def test_llm_adapter_passes_apps_function_name_to_code_prompt(self):
        class CapturingClient:
            model = "fake-model"

            def generate(self, messages, **_kwargs):
                self.prompt = messages[-1]["content"]
                return SimpleNamespace(content="def add(a, b): return a + b", model=self.model,
                                       finish_reason="stop", usage={})

        client = CapturingClient()
        operations = LLMOperations(client, SearchConfig(model="fake-model"))
        context = ProblemContext("apps", "test", "0000", "Add two values.",
                                 metadata={"function_name": "add"})
        operations.generate_code(context, SearchNode("root.1", thoughts=["Add arguments."]))
        self.assertIn("call-based", client.prompt)
        self.assertIn("`add`", client.prompt)
        self.assertNotIn("Read from stdin", client.prompt)

    def test_empty_stdout_diagnosis_reaches_feedback_and_rethink(self):
        class EmptyStdoutExecutor(FakeExecutor):
            def evaluate_public(self, context, code):
                return ExecutionReport(
                    dataset="apps", problem_id="0000", mode="stdin_stdout", status="failed",
                    passed_tests=0, total_tests=1, available_tests=3, duration_seconds=0.01,
                    tests=[TestCaseResult(index=0, status="wrong_answer", passed=False,
                                          duration_seconds=0.01, expected="YES\n", actual="")],
                )

            def trace_failure(self, context, code, failed_test_index):
                return "Only a function definition was executed."

        class CapturingLLM(FakeLLM):
            def analyze_feedback(self, context, node, code, failed_test, trace_text):
                self.failed_test = failed_test
                return super().analyze_feedback(context, node, code, failed_test, trace_text)

            def rethink(self, context, node, code, feedback):
                self.rethink_feedback = feedback
                return super().rethink(context, node, code, feedback)

        llm = CapturingLLM()
        context = ProblemContext("apps", "test", "0000", "Print YES.", public_test_count=1)
        result = SearchEngine(context, llm, EmptyStdoutExecutor(),
                              SearchConfig(rollouts=1, width=1, max_rethink_times=1)).run()
        self.assertEqual(result.candidates[0].feedback["diagnosis"].split(".")[0],
                         "The program finished with empty stdout although this test expects output")
        self.assertIn("reads stdin", llm.failed_test)
        self.assertIn("prints the answer", llm.rethink_feedback)

    def test_nonempty_stdout_rejects_contradictory_interface_feedback(self):
        class NonemptyExecutor(FakeExecutor):
            def evaluate_public(self, context, code):
                return ExecutionReport(
                    dataset="apps", problem_id="0000", mode="stdin_stdout", status="failed",
                    passed_tests=0, total_tests=1, available_tests=1, duration_seconds=0.01,
                    tests=[TestCaseResult(index=0, status="wrong_answer", passed=False,
                                          duration_seconds=0.01, expected="YES\n", actual="NO\n")],
                )

        class WrongFeedbackLLM(FakeLLM):
            def analyze_feedback(self, context, node, code, failed_test, trace_text):
                return '```json\n{"block":"interface","correct":false,"explanation":"No print call"}\n```'

        context = ProblemContext("apps", "test", "0000", "Print YES.", public_test_count=1)
        result = SearchEngine(context, WrongFeedbackLLM(), NonemptyExecutor(),
                              SearchConfig(rollouts=1, width=1, max_rethink_times=0)).run()
        feedback = result.candidates[0].feedback
        self.assertEqual(json.loads(feedback["analysis"])["block"], "output_mismatch")
        self.assertIn("non-empty stdout", feedback["analysis"])
        self.assertIn("No print call", feedback["discarded_analysis"])

    def test_trace_collects_runtime_locals(self):
        trace = collect_trace("def add(a, b):\n    total = a + b\n    return total\n", "_value = add(1, 2)")
        text = format_trace(trace)
        self.assertIn("line", text)
        self.assertIn("total", text)
        self.assertIn("before", text)
        self.assertIn("after", text)
        self.assertTrue(all("before" in event and "after" in event for block in trace.blocks for event in block.events))

    def test_trace_returns_feedback_for_invalid_python(self):
        for source, error_name in (
            ("def solve():\n    return ]\n", "SyntaxError"),
            ("    print(1)\n", "IndentationError"),
        ):
            with self.subTest(error_name=error_name):
                trace = collect_trace(source, "")
                self.assertEqual(trace.status, "syntax_error")
                self.assertEqual(trace.blocks, [])
                self.assertIn(error_name, format_trace(trace))

    def test_apps_test_workers_are_configurable(self):
        self.assertEqual(DatasetSearchExecutor(apps_test_workers=2).apps.test_workers, 2)
        with self.assertRaisesRegex(ValueError, "apps_test_workers"):
            SearchConfig(apps_test_workers=0).validate()

    def test_backpropagation_updates_entire_path_with_max_reward(self):
        root = SearchNode("root")
        parent = SearchNode("root.1", parent=root)
        leaf = SearchNode("root.1.1", parent=parent)
        root.add_child(parent)
        parent.add_child(leaf)
        leaf.backpropagate(0.7)
        leaf.backpropagate(0.4)
        self.assertEqual((root.visit_count, parent.visit_count, leaf.visit_count), (2, 2, 2))
        self.assertEqual((root.q_value, parent.q_value, leaf.q_value), (0.7, 0.7, 0.7))

    def test_rethink_resets_replaced_action_statistics_only(self):
        root = SearchNode("root")
        child = SearchNode("root.1", thoughts=["Old approach"], parent=root, prior=0.3)
        root.add_child(child)
        child.backpropagate(0.7)
        child.replace_last_thought("New approach")
        self.assertEqual((child.visit_count, child.q_value, child.prior), (0, 0.0, 1.0))
        self.assertEqual((root.visit_count, root.q_value), (1, 0.7))

    def test_llm_request_metadata_is_sanitized_and_emitted(self):
        events = []

        class Client:
            model = "fake-model"

            def generate(self, *_args, **_kwargs):
                return SimpleNamespace(
                    content="[]",
                    model="fake-model",
                    finish_reason="stop",
                    usage={"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5},
                )

        operations = LLMOperations(
            Client(),
            SearchConfig(model="fake-model"),
            on_call=events.append,
        )
        call = operations._call("expand", "private prompt must not be persisted")
        self.assertEqual(call.prompt_version, "native_v2/expand")
        self.assertEqual(events[0].metadata()["usage"]["total_tokens"], 5)
        self.assertNotIn("private prompt", events[0].metadata())

    def test_search_performs_feedback_and_in_place_rethink_without_deleting_old_candidate(self):
        context = ProblemContext(
            dataset="apps",
            split="test",
            problem_id="0000",
            statement="Return ok.",
            public_test_count=1,
            private_test_indices=(1,),
            total_test_count=2,
        )
        executor = FakeExecutor()
        engine = SearchEngine(
            context,
            FakeLLM(),
            executor,
            SearchConfig(rollouts=1, width=1, max_rethink_times=1),
        )
        result = engine.run()
        self.assertEqual(len(result.candidates), 2)
        self.assertEqual(result.candidates[0].status, "initial")
        self.assertEqual(result.candidates[1].status, "rethink")
        self.assertEqual(result.best_candidate.code, "good")
        self.assertEqual(executor.final_calls, 1)
        self.assertTrue(result.root.children)
        self.assertEqual(result.candidates[0].thoughts, ("Use a direct algorithm.",))
        self.assertEqual(result.candidates[1].thoughts, ("Handle the failing edge case explicitly.",))

    def test_rethink_retries_until_limit_and_expands_with_final_feedback(self):
        class AlwaysFail(FakeLLM):
            def __init__(self):
                super().__init__()
                self.rethink_calls = 0
                self.expansion_feedback = []

            def expand_thoughts(self, context, node, width):
                self.expansion_feedback.append(node.feedback)
                return super().expand_thoughts(context, node, width)

            def generate_code(self, context, node):
                return "bad"

            def rethink(self, context, node, code, feedback):
                self.rethink_calls += 1
                return f"Repair attempt {self.rethink_calls}."

        context = ProblemContext("apps", "test", "0000", "Return ok.", public_test_count=1)
        llm = AlwaysFail()
        result = SearchEngine(
            context, llm, FakeExecutor(),
            SearchConfig(rollouts=2, width=1, max_rethink_times=2),
        ).run()
        self.assertEqual(result.candidates[0].thoughts, ("Use a direct algorithm.",))
        self.assertEqual(result.candidates[1].thoughts, ("Repair attempt 1.",))
        self.assertEqual(result.candidates[2].thoughts, ("Repair attempt 2.",))
        self.assertEqual(llm.rethink_calls, 4)
        self.assertIsNone(llm.expansion_feedback[0])
        self.assertIsNotNone(llm.expansion_feedback[1])
        self.assertEqual(result.root.children[0].q_value, 0.0)

    def test_langgraph_routes_multiple_rollouts_to_finalization(self):
        context = ProblemContext("apps", "test", "0000", "Return ok.", public_test_count=1)
        events = []
        llm = FakeLLM()
        engine = SearchEngine(
            context,
            llm,
            FakeExecutor(),
            SearchConfig(rollouts=16, width=1, max_rethink_times=1),
            on_event=events.append,
        )
        self.assertTrue({"select", "expand", "evaluate", "rethink", "advance", "finalize"}.issubset(
            build_search_graph(engine).get_graph().nodes
        ))
        result = engine.run()
        self.assertEqual(len([event for event in events if event["event"] == "select"]), 16)
        self.assertEqual(len([event for event in events if event["event"] == "complete"]), 1)
        self.assertEqual(result.best_candidate.code, "good")

    def test_langgraph_skips_rethink_when_disabled(self):
        context = ProblemContext("apps", "test", "0000", "Return ok.", public_test_count=1)
        events = []
        result = SearchEngine(
            context,
            FakeLLM(),
            FakeExecutor(),
            SearchConfig(rollouts=1, width=1, max_rethink_times=0),
            on_event=events.append,
        ).run()
        self.assertEqual(len(result.candidates), 1)
        self.assertEqual(result.best_candidate.code, "bad")
        self.assertFalse(any(event["event"] in {"rethink", "rethink_next"} for event in events))

    def test_call_based_apps_trace_returns_block_feedback(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            problem = root / "apps" / "raw" / "test" / "0000"
            problem.mkdir(parents=True)
            (problem / "input_output.json").write_text(
                json.dumps({"fn_name": "add", "inputs": [[1, 2]], "outputs": [3]}),
                encoding="utf-8",
            )
            context = ProblemContext("apps", "test", "0000", "Add.", public_test_count=1)
            executor = DatasetSearchExecutor(root)
            trace = executor.trace_failure(context, "def add(a, b):\n    return a - b\n", 0)
            self.assertIn("BLOCK-", trace)

    def test_artifact_uses_candidate_thought_snapshot(self):
        context = ProblemContext("apps", "test", "0000", "Return ok.")
        candidate = CandidateRecord("candidate_0001", "root.1", "pass", 0, 1, 0.0, None, 0.0, "initial", thoughts=("Original",))
        with tempfile.TemporaryDirectory() as temp_dir:
            writer = ArtifactWriter(Path(temp_dir), context, SearchConfig(run_name="snapshot", model="fake"))
            writer.candidate(candidate)
            path = writer.candidates / candidate.candidate_id / "thoughts.json"
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), ["Original"])

    def test_artifact_resume_loads_without_provider(self):
        context = ProblemContext("apps", "test", "0000", "Return ok.", total_test_count=1)
        config = SearchConfig(run_name="resume", model="fake", rollouts=1)
        candidate = CandidateRecord("candidate_0001", "root.1.1", "print('ok')", 1, 1, 1.0, 0.5, 0.9, "initial", thoughts=("Use a direct solution.",))
        result = SearchResult(context, SearchNode("root"), [candidate], candidate, {"status": "passed"})
        with tempfile.TemporaryDirectory() as temp_dir:
            writer = ArtifactWriter(Path(temp_dir), context, config)
            writer.candidate(candidate)
            candidate_dir = Path(temp_dir) / "resume" / "fake" / "apps" / "0000" / "candidates" / candidate.candidate_id
            self.assertTrue((candidate_dir / "thoughts.json").is_file())
            writer.finalize(result, config, SimpleNamespace(calls=[], token_usage={}))
            resumed = ArtifactWriter(Path(temp_dir), context, config)
            self.assertTrue(resumed.is_complete())
            loaded = resumed.load_result(context)
            self.assertEqual(loaded.best_candidate.code, "print('ok')")


if __name__ == "__main__":
    unittest.main()
