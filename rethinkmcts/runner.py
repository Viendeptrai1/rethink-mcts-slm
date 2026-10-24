from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from ChatModels import ModalClient, ModalGpuClient, OllamaClient
from DataProcess import load_problem
from Executors import AppsExecutor, HumanevalExecutor
from Executors.common import ExecutionReport, TestCaseResult, build_report, run_python_source

from .config import SearchConfig
from .feedback.trace import collect_trace, format_trace
from .parsing import parse_score, parse_thoughts
from .prompts import (
    code_prompt,
    expand_prompt,
    feedback_prompt,
    rethink_prompt,
    self_evaluation_prompt,
)
from .search import ProblemContext, SearchEngine, SearchResult
from .tree import CandidateRecord, SearchNode


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_ROOT = PROJECT_ROOT / "data"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "outputs" / "rethinkmcts"


@dataclass(frozen=True)
class LLMCall:
    request_id: str
    operation: str
    content: str
    model: str
    finish_reason: str | None
    usage: dict[str, int | None]
    prompt_version: str

    def metadata(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "operation": self.operation,
            "prompt_version": self.prompt_version,
            "model": self.model,
            "finish_reason": self.finish_reason,
            "usage": self.usage,
        }


class LLMOperations:
    def __init__(
        self,
        client: Any,
        config: SearchConfig,
        *,
        on_call: Any | None = None,
    ) -> None:
        self.client = client
        self.config = config
        self.on_call = on_call or (lambda call: None)
        self.model = config.model or getattr(client, "model", None) or "configured-model"
        self.calls: list[LLMCall] = []

    def _call(self, operation: str, prompt: str, *, max_tokens: int | None = None) -> LLMCall:
        selected_model = (
            self.config.evaluator_model
            if operation == "self_evaluation" and self.config.evaluator_model
            else self.config.model
        )
        result = self.client.generate(
            [
                {"role": "system", "content": "You are an expert programming assistant."},
                {"role": "user", "content": prompt},
            ],
            model=selected_model,
            max_tokens=self.config.max_tokens if max_tokens is None else max_tokens,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            reasoning_effort=self.config.reasoning_effort,
        )
        call = LLMCall(
            request_id=f"request_{len(self.calls) + 1:04d}",
            operation=operation,
            content=result.content,
            model=result.model,
            finish_reason=result.finish_reason,
            usage=dict(result.usage or {}),
            prompt_version=f"native_v2/{operation}",
        )
        self.calls.append(call)
        self.on_call(call)
        return call

    def expand_thoughts(self, context: ProblemContext, node: SearchNode, width: int):
        feedback = json.dumps(node.feedback, ensure_ascii=False) if node.feedback else None
        response = self._call(
            "expand",
            expand_prompt(
                context.statement,
                node.thoughts,
                feedback=feedback,
                width=width,
                starter_code=context.starter_code,
                dataset=context.dataset,
                function_name=context.metadata.get("function_name"),
            ),
        )
        return parse_thoughts(response.content, width=width)

    def generate_code(self, context: ProblemContext, node: SearchNode) -> LLMCall:
        return self._call(
            "code_generation",
            code_prompt(
                context.statement, node.thoughts,
                starter_code=context.starter_code, dataset=context.dataset,
                function_name=context.metadata.get("function_name"),
            ),
        )

    def self_evaluate(self, context: ProblemContext, node: SearchNode, code: str) -> float:
        response = self._call(
            "self_evaluation",
            self_evaluation_prompt(context.statement, node.thoughts, code),
            max_tokens=256,
        )
        return parse_score(response.content)

    def analyze_feedback(
        self,
        context: ProblemContext,
        node: SearchNode,
        code: str,
        failed_test: str,
        trace_text: str,
    ) -> str:
        response = self._call(
            "verbal_feedback",
            feedback_prompt(
                context.statement, node.thoughts, code, failed_test, trace_text,
                dataset=context.dataset, function_name=context.metadata.get("function_name"),
            ),
            max_tokens=1024,
        )
        return response.content

    def rethink(self, context: ProblemContext, node: SearchNode, code: str, feedback: str) -> LLMCall:
        return self._call(
            "rethink",
            rethink_prompt(
                context.statement, node.thoughts, code, feedback,
                dataset=context.dataset, function_name=context.metadata.get("function_name"),
            ),
            max_tokens=512,
        )

    @property
    def token_usage(self) -> dict[str, int]:
        totals = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        for call in self.calls:
            for key in totals:
                value = call.usage.get(key)
                if value is not None:
                    totals[key] += int(value)
        return totals


def _parse_numeric_id(problem_id: str | int) -> int:
    match = re.search(r"\d+", str(problem_id))
    if match is None:
        raise ValueError(f"Problem ID is not numeric: {problem_id}")
    return int(match.group(0))


def load_context(
    dataset: str,
    problem_id: str | int,
    *,
    data_root: str | Path = DEFAULT_DATA_ROOT,
    public_cases_type: str = "half",
) -> ProblemContext:
    root = Path(data_root)
    normalized = dataset.lower()
    if normalized == "apps":
        problem = load_problem("apps", str(problem_id), split="test", data_root=root)
        numeric_id = int(problem.problem_id)
        test_path = root / "apps" / "raw" / "test" / f"{numeric_id:04d}" / "input_output.json"
        payload = json.loads(test_path.read_text(encoding="utf-8"))
        inputs = payload.get("inputs", [])
        outputs = payload.get("outputs", [])
        total = len(inputs)
        if public_cases_type == "half":
            public_count = total // 2
        elif public_cases_type == "half_min2":
            public_count = max(2, total // 2)
        else:
            public_count = int(public_cases_type)
        if public_count <= 0 or public_count >= total:
            raise ValueError(f"APPS problem {numeric_id:04d} cannot split {total} tests into public/private")
        return ProblemContext(
            dataset="apps",
            split="test",
            problem_id=f"{numeric_id:04d}",
            statement=problem.statement,
            starter_code=problem.starter_code,
            public_test_count=public_count,
            public_policy=public_cases_type,
            private_test_indices=tuple(range(public_count, total)),
            total_test_count=total,
            metadata={
                "function_name": payload.get("fn_name"),
                "input_output_path": str(test_path),
            },
        )

    if normalized == "humaneval":
        numeric_id = _parse_numeric_id(problem_id)
        from datasets import load_from_disk

        dataset_obj = load_from_disk(str(root / "humaneval" / "arrow"))["test"]
        row = dataset_obj[numeric_id]
        prompt = str(row["prompt"])
        public_path = root / "humaneval" / "public_tests.jsonl"
        with public_path.open("r", encoding="utf-8") as source:
            public_rows = [json.loads(line) for line in source if line.strip()]
        if len(public_rows) != len(dataset_obj):
            raise ValueError("HumanEval public-test file does not match the Arrow dataset")
        public_row = public_rows[numeric_id]
        if (public_row.get("task_id") != row["task_id"] or
                public_row.get("entry_point") != row["entry_point"]):
            raise ValueError(f"HumanEval public-test identity mismatch: {numeric_id}")
        given_tests = tuple(public_row.get("given_tests") or ())
        if not given_tests:
            raise ValueError(f"HumanEval/{numeric_id} has no public tests")
        return ProblemContext(
            dataset="humaneval",
            split="test",
            problem_id=str(row["task_id"]),
            statement=prompt,
            entry_point=str(row["entry_point"]),
            public_test_count=len(given_tests),
            public_policy="given_tests",
            private_test_indices=(),
            total_test_count=1,
            public_tests=given_tests,
            metadata={"task_id": str(row["task_id"]), "public_tests_source": "pinned_peer_given_tests"},
        )
    raise ValueError("dataset must be 'apps' or 'humaneval'")


class DatasetSearchExecutor:
    def __init__(
        self,
        data_root: str | Path = DEFAULT_DATA_ROOT,
        *,
        timeout_seconds: float = 5.0,
        apps_test_workers: int = 1,
        max_trace_blocks: int = 10,
        max_block_chars: int = 5000,
    ) -> None:
        self.data_root = Path(data_root)
        self.timeout_seconds = timeout_seconds
        self.max_trace_blocks = max_trace_blocks
        self.max_block_chars = max_block_chars
        self.apps = AppsExecutor(
            self.data_root / "apps" / "raw",
            timeout_per_test=timeout_seconds,
            test_workers=apps_test_workers,
        )
        self.humaneval = HumanevalExecutor(
            self.data_root / "humaneval" / "arrow",
            timeout=timeout_seconds,
        )

    def evaluate_public(self, context: ProblemContext, code: str) -> ExecutionReport:
        if context.dataset == "apps":
            return self.apps.evaluate(code, context.problem_id, max_tests=context.public_test_count)
        return self._evaluate_humaneval_public(context, code)

    def evaluate_private(self, context: ProblemContext, code: str) -> ExecutionReport:
        if context.dataset == "apps":
            return self.apps.evaluate(
                code,
                context.problem_id,
                test_indices=list(context.private_test_indices),
            )
        return self.humaneval.evaluate(code, context.problem_id)

    def evaluate_final(self, context: ProblemContext, code: str) -> ExecutionReport:
        if context.dataset == "apps":
            return self.apps.evaluate(code, context.problem_id)
        return self.humaneval.evaluate(code, context.problem_id)

    def _evaluate_humaneval_public(self, context: ProblemContext, code: str) -> ExecutionReport:
        tests: list[TestCaseResult] = []
        for index, assertion in enumerate(context.public_tests):
            source = f"{code.rstrip()}\n\n{assertion}\n"
            process = run_python_source(source, timeout_seconds=self.timeout_seconds)
            if process.status == "timeout":
                status = "timeout"
                error = "Execution exceeded the public-test timeout"
            elif process.returncode != 0:
                status = "wrong_answer" if "AssertionError" in process.stderr else "runtime_error"
                error = process.stderr.strip() or "public test failed"
            else:
                status = "passed"
                error = None
            tests.append(
                TestCaseResult(
                    index=index,
                    status=status,
                    passed=status == "passed",
                    duration_seconds=process.duration_seconds,
                    error=error,
                    expected=assertion,
                    actual=process.stdout.strip() or None,
                )
            )
        return build_report(
            dataset="humaneval",
            problem_id=context.problem_id,
            mode="given_tests",
            available_tests=len(context.public_tests),
            tests=tests,
        )

    def trace_failure(self, context: ProblemContext, code: str, failed_test_index: int) -> str:
        if context.dataset == "humaneval":
            if failed_test_index < 0 or failed_test_index >= len(context.public_tests):
                return "No replayable HumanEval public test was returned."
            driver = context.public_tests[failed_test_index]
            trace = collect_trace(code, driver, timeout_seconds=self.timeout_seconds)
            return format_trace(
                trace,
                max_blocks=self.max_trace_blocks,
                max_chars=self.max_block_chars,
            )

        problem_dir = self.data_root / "apps" / "raw" / "test" / context.problem_id
        payload = json.loads((problem_dir / "input_output.json").read_text(encoding="utf-8"))
        inputs = payload.get("inputs", [])
        if failed_test_index < 0 or failed_test_index >= len(inputs):
            return "No replayable APPS public test was returned."
        function_name = payload.get("fn_name")
        if function_name:
            argument = inputs[failed_test_index]
            driver = (
                f"target = globals().get({function_name!r})\n"
                f"if target is None and 'Solution' in globals(): target = getattr(Solution(), {function_name!r})\n"
                f"_rethink_result = target(*{argument!r} if isinstance({argument!r}, list) else [{argument!r}])"
            )
            trace = collect_trace(code, driver, timeout_seconds=self.timeout_seconds)
        else:
            raw_input = inputs[failed_test_index]
            if isinstance(raw_input, list):
                raw_input = "\n".join(str(item) for item in raw_input)
            trace = collect_trace(code, "", stdin=str(raw_input), timeout_seconds=self.timeout_seconds)
        return format_trace(
            trace,
            max_blocks=self.max_trace_blocks,
            max_chars=self.max_block_chars,
        )


class ArtifactWriter:
    def __init__(self, root: Path, context: ProblemContext, config: SearchConfig) -> None:
        safe_model = _safe_component(config.model or "configured-model")
        self.directory = root / _safe_component(config.run_name) / safe_model / context.dataset / _safe_component(context.problem_id)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.candidates = self.directory / "candidates"
        self.candidates.mkdir(exist_ok=True)
        self.events_path = self.directory / "events.jsonl"
        if not self.events_path.exists():
            self.events_path.write_text("", encoding="utf-8")

    def is_complete(self) -> bool:
        return (self.directory / "search_summary.json").is_file() and (
            self.directory / "final_solution.py"
        ).is_file()

    def load_result(self, context: ProblemContext) -> SearchResult:
        summary = json.loads((self.directory / "search_summary.json").read_text(encoding="utf-8"))
        code = (self.directory / "final_solution.py").read_text(encoding="utf-8").rstrip()
        candidate = CandidateRecord(
            candidate_id=str(summary.get("best_candidate_id") or "resumed_candidate"),
            node_id="resumed",
            code=code,
            public_passed_tests=0,
            public_total_tests=0,
            public_pass_rate=0.0,
            llm_score=None,
            reward=float(summary.get("best_reward") or 0.0),
            status="resumed",
            execution=None,
        )
        return SearchResult(
            context=context,
            root=SearchNode(node_id="root"),
            candidates=[candidate],
            best_candidate=candidate,
            private_evaluation=summary.get("final_evaluation") or summary.get("private_evaluation"),
        )

    def event(self, event: dict[str, Any]) -> None:
        with self.events_path.open("a", encoding="utf-8") as output:
            output.write(json.dumps(event, ensure_ascii=False) + "\n")

    def candidate(self, candidate: CandidateRecord) -> None:
        directory = self.candidates / candidate.candidate_id
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "solution.py").write_text(candidate.code.rstrip() + "\n", encoding="utf-8")
        (directory / "response.txt").write_text(
            candidate.response_text or candidate.code,
            encoding="utf-8",
        )
        (directory / "thoughts.json").write_text(
            json.dumps(candidate.thoughts, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (directory / "execution.json").write_text(
            json.dumps(candidate.execution, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (directory / "feedback.json").write_text(
            json.dumps(candidate.feedback, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (directory / "metadata.json").write_text(
            json.dumps(
                {
                    "candidate_id": candidate.candidate_id,
                    "node_id": candidate.node_id,
                    "thoughts": list(candidate.thoughts),
                    "public_pass_rate": candidate.public_pass_rate,
                    "llm_score": candidate.llm_score,
                    "reward": candidate.reward,
                    "status": candidate.status,
                    "request_ids": candidate.request_ids,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def finalize(self, result: SearchResult, config: SearchConfig, llm: LLMOperations) -> None:
        (self.directory / "tree.json").write_text(
            json.dumps(result.root.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        if result.best_candidate is not None:
            (self.directory / "final_solution.py").write_text(
                result.best_candidate.code.rstrip() + "\n",
                encoding="utf-8",
            )
        summary = result.to_summary(config, len(llm.calls), llm.token_usage)
        summary["llm_requests"] = [call.metadata() for call in llm.calls]
        summary["created_at"] = datetime.now(timezone.utc).isoformat()
        (self.directory / "search_summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def _safe_component(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._") or "unnamed"


def configured_client(config: SearchConfig) -> Any:
    load_dotenv(PROJECT_ROOT / ".env")
    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
    if provider == "ollama":
        return OllamaClient(str(PROJECT_ROOT / ".env"))
    if provider == "modal":
        return ModalClient(str(PROJECT_ROOT / ".env"))
    if provider == "modal_gpu":
        return ModalGpuClient(str(PROJECT_ROOT / ".env"))
    raise ValueError("LLM_PROVIDER must be ollama, modal or modal_gpu")


def run_search(
    *,
    context: ProblemContext,
    config: SearchConfig,
    data_root: str | Path = DEFAULT_DATA_ROOT,
    output_root: str | Path = DEFAULT_OUTPUT_ROOT,
) -> SearchResult:
    writer = ArtifactWriter(Path(output_root), context, config)
    if writer.is_complete():
        return writer.load_result(context)
    client = configured_client(config)
    llm = LLMOperations(
        client,
        config,
        on_call=lambda call: writer.event({"event": "llm_request", **call.metadata()}),
    )
    executor = DatasetSearchExecutor(
        data_root,
        timeout_seconds=config.timeout_seconds,
        apps_test_workers=config.apps_test_workers,
        max_trace_blocks=config.max_trace_blocks,
        max_block_chars=config.max_block_chars,
    )

    def on_event(event: dict[str, Any]) -> None:
        writer.event(event)

    result = SearchEngine(context, llm, executor, config, on_event=on_event).run()
    for candidate in result.candidates:
        writer.candidate(candidate)
    writer.finalize(result, config, llm)
    return result
