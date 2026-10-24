from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Protocol

from Executors.common import ExecutionReport

from .config import SearchConfig
from .parsing import ThoughtProposal, extract_code, parse_feedback
from .reward import compute_reward
from .tree import CandidateRecord, SearchNode


@dataclass(frozen=True)
class ProblemContext:
    dataset: str
    split: str
    problem_id: str
    statement: str
    starter_code: str = ""
    entry_point: str | None = None
    public_test_count: int = 0
    public_policy: str = "unspecified"
    private_test_indices: tuple[int, ...] = ()
    total_test_count: int = 0
    public_tests: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset": self.dataset,
            "split": self.split,
            "problem_id": self.problem_id,
            "entry_point": self.entry_point,
            "public_test_count": self.public_test_count,
            "private_test_count": len(self.private_test_indices),
            "total_test_count": self.total_test_count,
            "public_policy": self.public_policy,
            "metadata": self.metadata,
        }


class SearchLLM(Protocol):
    def expand_thoughts(self, context: ProblemContext, node: SearchNode, width: int) -> list[ThoughtProposal]: ...

    def generate_code(self, context: ProblemContext, node: SearchNode) -> Any: ...

    def self_evaluate(self, context: ProblemContext, node: SearchNode, code: str) -> float: ...

    def analyze_feedback(
        self,
        context: ProblemContext,
        node: SearchNode,
        code: str,
        failed_test: str,
        trace_text: str,
    ) -> str: ...

    def rethink(
        self,
        context: ProblemContext,
        node: SearchNode,
        code: str,
        feedback: str,
    ) -> Any: ...


class SearchExecutor(Protocol):
    def evaluate_public(self, context: ProblemContext, code: str) -> ExecutionReport: ...

    def evaluate_private(self, context: ProblemContext, code: str) -> ExecutionReport: ...

    def evaluate_final(self, context: ProblemContext, code: str) -> ExecutionReport: ...

    def trace_failure(self, context: ProblemContext, code: str, failed_test_index: int) -> str: ...


@dataclass(frozen=True)
class SearchResult:
    context: ProblemContext
    root: SearchNode
    candidates: list[CandidateRecord]
    best_candidate: CandidateRecord | None
    private_evaluation: dict[str, Any] | None

    def to_summary(self, config: SearchConfig, request_count: int, token_usage: dict[str, int]) -> dict[str, Any]:
        best = self.best_candidate
        return {
            "run_name": config.run_name,
            "model": config.model,
            "dataset": self.context.dataset,
            "problem_id": self.context.problem_id,
            "config": asdict(config),
            "problem": self.context.to_dict(),
            "candidate_count": len(self.candidates),
            "request_count": request_count,
            "token_usage": token_usage,
            "rethink_count": sum(candidate.status == "rethink" for candidate in self.candidates),
            "best_candidate_id": best.candidate_id if best else None,
            "best_reward": best.reward if best else None,
            "final_evaluation": self.private_evaluation,
            "private_evaluation": self.private_evaluation,
        }


class SearchEngine:
    def __init__(
        self,
        context: ProblemContext,
        llm: SearchLLM,
        executor: SearchExecutor,
        config: SearchConfig,
        *,
        on_event: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        config.validate()
        self.context = context
        self.llm = llm
        self.executor = executor
        self.config = config
        self.on_event = on_event or (lambda event: None)
        self._candidate_number = 0
        self.candidates: list[CandidateRecord] = []
        self.rng = random.Random(config.seed)

    def _event(self, kind: str, **payload: Any) -> None:
        self.on_event({"event": kind, **payload})

    @staticmethod
    def _call_content(value: Any) -> str:
        return str(getattr(value, "content", value))

    def _expand(self, node: SearchNode) -> None:
        proposals = self.llm.expand_thoughts(self.context, node, self.config.width)
        if len(proposals) != self.config.width:
            raise ValueError(f"Expansion returned {len(proposals)} thoughts; expected {self.config.width}")
        node.expansion_count += 1
        for index, proposal in enumerate(proposals):
            child = SearchNode(
                node_id=f"{node.node_id}.{index + 1}.{node.expansion_count}",
                thoughts=[*node.thoughts, proposal.thought],
                parent=node,
                prior=proposal.reasonableness,
                action=proposal.thought,
            )
            node.add_child(child)
        self._event(
            "expand",
            node_id=node.node_id,
            children=[
                {"node_id": child.node_id, "thought": child.action, "prior": child.prior}
                for child in node.children
            ],
        )

    def _failed_test_text(self, report: ExecutionReport) -> tuple[int, str, str | None]:
        for test in report.tests:
            if not test.passed:
                diagnosis = None
                if (report.dataset == "apps" and report.mode == "stdin_stdout"
                        and test.status == "wrong_answer"
                        and isinstance(test.actual, str) and not test.actual.strip()
                        and test.expected is not None
                        and (not isinstance(test.expected, str) or test.expected.strip())):
                    diagnosis = (
                        "The program finished with empty stdout although this test expects "
                        "output. Check that it reads stdin, calls its solver, and prints the answer."
                    )
                return test.index, json.dumps(
                    {
                        "index": test.index,
                        "status": test.status,
                        "expected": test.expected,
                        "actual": test.actual,
                        "error": test.error,
                        "diagnosis": diagnosis,
                    },
                    ensure_ascii=False,
                ), diagnosis
        return -1, "No failed test details were returned by the executor.", None

    def _evaluate(self, node: SearchNode, *, phase: str) -> CandidateRecord:
        raw_code = self.llm.generate_code(self.context, node)
        response_text = self._call_content(raw_code)
        code = extract_code(response_text)
        if not code:
            raise ValueError(f"Code generation returned an empty response for {node.node_id}")
        node.candidate_code = code
        public_report = self.executor.evaluate_public(self.context, code)
        pass_rate = public_report.pass_rate
        llm_score = None
        if pass_rate == 1.0 and self.config.reward_mode == "dual":
            llm_score = self.llm.self_evaluate(self.context, node, code)
        if self.config.reward_mode == "test_only":
            reward = pass_rate
        else:
            reward = compute_reward(
                pass_rate, llm_score, a=self.config.reward_a, b=self.config.reward_b
            )
        feedback: dict[str, Any] | None = None
        if pass_rate < 1.0:
            failed_index, failed_text, diagnosis = self._failed_test_text(public_report)
            trace_text = self.executor.trace_failure(self.context, code, failed_index)
            analysis = self.llm.analyze_feedback(
                self.context,
                node,
                code,
                failed_text,
                trace_text,
            )
            analysis_raw = None
            failed_case = next((test for test in public_report.tests if not test.passed), None)
            if (public_report.dataset == "apps" and public_report.mode == "stdin_stdout"
                    and failed_case is not None and isinstance(failed_case.actual, str)
                    and failed_case.actual.strip()
                    and str(parse_feedback(analysis).get("block", "")).lower() == "interface"):
                analysis_raw = analysis
                analysis = json.dumps({
                    "block": "output_mismatch",
                    "correct": False,
                    "explanation": (
                        "The executor observed non-empty stdout, so a missing print or "
                        "entrypoint cannot explain this failure. Compare the expected and "
                        "actual outputs; inspect input parsing, output format, and algorithm."
                    ),
                })
            feedback = {
                "failed_test_index": failed_index,
                "failed_test": failed_text,
                "trace": trace_text,
                "analysis": analysis,
                "diagnosis": diagnosis,
            }
            if analysis_raw is not None:
                feedback["discarded_analysis"] = analysis_raw
            node.feedback = feedback
        else:
            node.feedback = None
        self._candidate_number += 1
        candidate = CandidateRecord(
            candidate_id=f"candidate_{self._candidate_number:04d}",
            node_id=node.node_id,
            code=code,
            public_passed_tests=public_report.passed_tests,
            public_total_tests=public_report.total_tests,
            public_pass_rate=pass_rate,
            llm_score=llm_score,
            reward=reward,
            status=phase,
            feedback=feedback,
            request_ids=[
                request_id
                for request_id in [getattr(raw_code, "request_id", None)]
                if request_id
            ],
            response_text=response_text,
            execution=public_report.to_dict(),
            thoughts=tuple(node.thoughts),
        )
        self.candidates.append(candidate)
        node.backpropagate(reward)
        self._event(
            "evaluate",
            phase=phase,
            candidate_id=candidate.candidate_id,
            node_id=node.node_id,
            public_pass_rate=pass_rate,
            llm_score=llm_score,
            reward=reward,
        )
        return candidate

    def _rethink(self, node: SearchNode, candidate: CandidateRecord) -> bool:
        if candidate.public_pass_rate >= 1.0 or node.rethink_count >= self.config.max_rethink_times:
            return False
        feedback_text = json.dumps(candidate.feedback or {}, ensure_ascii=False)
        replacement = self._call_content(
            self.llm.rethink(self.context, node, candidate.code, feedback_text)
        ).strip()
        if not replacement:
            return False
        node.replace_last_thought(replacement, feedback=candidate.feedback)
        self._event("rethink", node_id=node.node_id, replacement=replacement)
        return True

    def run(self) -> SearchResult:
        from .workflow import WorkflowState, build_search_graph

        root = SearchNode(node_id="root")
        recursion_limit = max(25, self.config.rollouts * (4 + 2 * self.config.max_rethink_times) + 10)
        state = WorkflowState.model_validate(
            build_search_graph(self).invoke(
                WorkflowState(root=root),
                {"recursion_limit": recursion_limit},
            )
        )
        return SearchResult(
            context=self.context,
            root=root,
            candidates=self.candidates,
            best_candidate=state.best_candidate,
            private_evaluation=state.private_evaluation,
        )
