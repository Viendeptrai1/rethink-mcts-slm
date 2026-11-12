"""
SemanticPromptedLLM implementing semantic model ports using Jinja2 templates and ModelGateway.
"""

import json
import logging
import os
import re
import uuid
from dataclasses import replace
from rethink_mcts.config import SamplingConfig
from rethink_mcts.application.model_calls import complete_request
from typing import Optional
from jinja2 import Environment, FileSystemLoader, StrictUndefined, Undefined

from rethink_mcts.domain.problem import ExecutionSpec
from rethink_mcts.domain.tree import ProposalBatch
from rethink_mcts.domain.feedback import (
    ExecutionFacts,
    TraceResult,
    BlockAnalysis,
    BlockAssessment,
    BlockVerdict,
    VerbalFeedback
)
from rethink_mcts.ports.models import (
    GenerationRequest,
    ModelGateway,
    ThoughtProposer,
    CodeGenerator,
    ThoughtRefiner,
    CodeCritic,
    BlockAnalyzer
)
from rethink_mcts.adapters.llm.parsing import (
    parse_thoughts_json,
    extract_python_code,
    parse_critic_score
)
from rethink_mcts.policies.prior import PriorPolicy

logger = logging.getLogger(__name__)


def interface_context(execution_spec: Optional[ExecutionSpec]) -> dict:
    """Variables describing the execution interface, passed to every template."""
    if execution_spec is None:
        return dict(mode=None, entry_point=None, starter_code=None)
    mode = execution_spec.mode.value if hasattr(execution_spec.mode, "value") else str(execution_spec.mode)
    return dict(mode=mode, entry_point=execution_spec.entry_point, starter_code=execution_spec.starter_code)


def format_failed_test(facts: ExecutionFacts) -> str:
    """Human-readable description of the first failed public test."""
    parts = [f"Result: {facts.failure_kind} ({facts.public_passed}/{facts.public_total} public tests passed)",
             f"Input:\n{facts.input_snippet}",
             f"Expected output:\n{facts.expected_output_snippet}",
             f"Actual output:\n{facts.actual_output_snippet}"]
    if facts.traceback_snippet:
        parts.append(f"Error:\n{facts.traceback_snippet}")
    return "\n".join(parts)


def _verdict(item: dict) -> BlockVerdict:
    if "correct" in item:
        value = item["correct"]
        if isinstance(value, bool):
            return BlockVerdict.CORRECT if value else BlockVerdict.INCORRECT
        text = str(value).strip().lower()
        if text in ("true", "1", "yes"):
            return BlockVerdict.CORRECT
        if text in ("false", "0", "no"):
            return BlockVerdict.INCORRECT
        return BlockVerdict.UNKNOWN
    text = str(item.get("verdict", "unknown")).strip().lower()
    return BlockVerdict.CORRECT if text == "correct" else (
        BlockVerdict.INCORRECT if text == "incorrect" else BlockVerdict.UNKNOWN)


def parse_block_analysis(content: str) -> tuple[tuple[BlockAssessment, ...], str]:
    """Parse a block-analysis response.

    Accepts a single object ``{block, correct, explanation}`` (what the prompt asks for),
    a list of such objects, or a wrapper with ``assessments``/``blocks``/``analysis``.
    Returns (assessments, summary). Raises ValueError if no JSON can be read; the caller
    then keeps the raw text, as upstream RethinkMCTS does.
    """
    cleaned = content.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if match:
        cleaned = match.group(1).strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # The paper's example answer is a sequence of objects, not a list: decode them one by one.
        decoder, values, pos = json.JSONDecoder(), [], 0
        while True:
            starts = [i for i in (cleaned.find("{", pos), cleaned.find("[", pos)) if i >= 0]
            if not starts:
                break
            try:
                value, pos = decoder.raw_decode(cleaned, min(starts))
            except json.JSONDecodeError:
                pos = min(starts) + 1
                continue
            values.extend(value if isinstance(value, list) else [value])
        if not values:
            raise ValueError("no JSON object in block analysis output")
        data = values
    summary = ""
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        summary = str(data.get("summary", ""))
        if any(k in data for k in ("assessments", "blocks", "analysis")):
            items = data.get("assessments", data.get("blocks", data.get("analysis", [])))
        elif any(k in data for k in ("block", "block_id")):
            items = [data]
        else:
            items = []
    else:
        raise ValueError("block analysis JSON is neither an object nor a list")
    assessments = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        block_id = str(item.get("block_id", item.get("block", "")))
        explanation = str(item.get("explanation", item.get("reason", "")))
        assessments.append(BlockAssessment(block_id=block_id, verdict=_verdict(item), explanation=explanation))
    return tuple(assessments), summary


class SemanticPromptedLLM(
    ThoughtProposer,
    CodeGenerator,
    ThoughtRefiner,
    CodeCritic,
    BlockAnalyzer
):
    """
    Renders prompts from Jinja2 templates, calls ModelGateway, and parses structured output.
    With strict_variables=True a template that references a variable the code does not
    pass raises an error instead of silently rendering an empty string.
    """
    def __init__(
        self,
        gateway: ModelGateway,
        prompts_dir: str = "prompts/compact_v1",
        prior_policy: Optional[PriorPolicy] = None,
        sampling=None, seed=None, critic_min=0.0, critic_max=1.0, max_prompt_blocks=32,
        require_exact_token_count=False, strict_variables=False
    ):
        self.gateway = gateway
        self.sampling = sampling or SamplingConfig()
        self.seed = seed
        self.critic_min, self.critic_max = critic_min, critic_max
        self.max_prompt_blocks = max_prompt_blocks
        self.meters_requests = True
        self.budget = None
        self.require_exact_token_count = require_exact_token_count
        self.prompts_dir = prompts_dir
        self.prior_policy = prior_policy or PriorPolicy()

        if not os.path.exists(prompts_dir):
            # Fallback to TLCN relative path
            base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            self.prompts_dir = os.path.join(base, prompts_dir)

        self.env = Environment(loader=FileSystemLoader(self.prompts_dir),
                               undefined=StrictUndefined if strict_variables else Undefined)

    def _render(self, name: str, **variables) -> str:
        return self.env.get_template(name).render(**variables)

    def propose(
        self,
        statement: str,
        active_thoughts: tuple[str, ...],
        width: int,
        feedback: Optional[VerbalFeedback] = None,
        execution_spec: Optional[ExecutionSpec] = None
    ) -> ProposalBatch:
        prompt = self._render("expand.jinja",
            statement=statement,
            active_thoughts=list(active_thoughts),
            width=width,
            feedback_text=feedback.format_as_text() if feedback else "",
            **interface_context(execution_spec)
        )

        req = GenerationRequest(
            request_id=f"req_exp_{uuid.uuid4().hex[:8]}",
            role="expansion",
            prompt=prompt,
            response_contract="json"
        )
        resp = self._complete(req)

        raw_proposals = parse_thoughts_json(resp.content)
        processed = self.prior_policy.process_raw_proposals(raw_proposals[:width])

        return ProposalBatch(
            batch_id=str(uuid.uuid4()),
            proposals=tuple(processed[:width]),
            raw_response_ref=resp.raw_response_ref
        )

    def generate(
        self,
        statement: str,
        execution_spec: ExecutionSpec,
        active_thoughts: tuple[str, ...],
        public_examples_str: str = ""
    ) -> str:
        prompt = self._render("generate_code.jinja",
            statement=statement,
            active_thoughts=list(active_thoughts),
            public_examples=public_examples_str,
            **interface_context(execution_spec)
        )

        req = GenerationRequest(
            request_id=f"req_gen_{uuid.uuid4().hex[:8]}",
            role="code",
            prompt=prompt
        )
        resp = self._complete(req)
        return extract_python_code(resp.content)

    def refine(
        self,
        statement: str,
        execution_spec: ExecutionSpec,
        parent_thoughts: tuple[str, ...],
        erroneous_thought: str,
        candidate_code: str,
        feedback: VerbalFeedback
    ) -> str:
        prompt = self._render("rethink.jinja",
            statement=statement,
            parent_thoughts=list(parent_thoughts),
            erroneous_thought=erroneous_thought,
            active_thoughts=[*parent_thoughts, erroneous_thought],
            candidate_code=candidate_code,
            feedback_text=feedback.format_as_text(),
            **interface_context(execution_spec)
        )

        req = GenerationRequest(
            request_id=f"req_reth_{uuid.uuid4().hex[:8]}",
            role="rethink",
            prompt=prompt
        )
        resp = self._complete(req)
        return resp.content.strip()

    def assess(
        self,
        statement: str,
        candidate_code: str,
        active_thoughts: tuple[str, ...] = ()
    ) -> float:
        prompt = self._render("self_eval.jinja",
            statement=statement,
            candidate_code=candidate_code,
            active_thoughts=list(active_thoughts),
            score_min=self.critic_min,
            score_max=self.critic_max
        )

        req = GenerationRequest(
            request_id=f"req_crit_{uuid.uuid4().hex[:8]}",
            role="critic",
            prompt=prompt,
            response_contract="json"
        )
        resp = self._complete(req)
        return parse_critic_score(resp.content, score_min=self.critic_min, score_max=self.critic_max)

    def analyze(
        self,
        statement: str,
        candidate_code: str,
        facts: ExecutionFacts,
        trace: TraceResult,
        execution_spec: Optional[ExecutionSpec] = None,
        active_thoughts: tuple[str, ...] = ()
    ) -> BlockAnalysis:
        trace_snippets = []
        for v in trace.block_visits[:self.max_prompt_blocks]:
            before_str = ", ".join(f"{k}={val}" for k, val in v.locals_before.items()) if v.locals_before else "none"
            after_str = ", ".join(f"{k}={val}" for k, val in v.locals_after.items()) if v.locals_after else "none"
            exit_note = f" (exit: {v.exit_kind})" if v.exit_kind and v.exit_kind != "fallthrough" else ""
            trace_snippets.append(
                f"[{v.block_id}{exit_note}]\n# Locals before: {before_str}\n{v.source_snippet.strip()}\n# Locals after: {after_str}"
            )
        if trace.omitted_visits_count:
            trace_snippets.append(f"... ({trace.omitted_visits_count} later block visits omitted)")
        failed_test = format_failed_test(facts)

        prompt = self._render("analyze_block.jinja",
            statement=statement,
            candidate_code=candidate_code,
            active_thoughts=list(active_thoughts),
            failed_test=failed_test,
            facts_text=failed_test,
            trace_text="\n\n".join(trace_snippets),
            **interface_context(execution_spec)
        )

        req = GenerationRequest(
            request_id=f"req_anlz_{uuid.uuid4().hex[:8]}",
            role="block_analysis",
            prompt=prompt,
            response_contract="json"
        )
        resp = self._complete(req)
        raw_text = resp.content.strip()
        try:
            assessments, summary = parse_block_analysis(raw_text)
        except (ValueError, json.JSONDecodeError) as exc:
            logger.warning("Block analysis is not valid JSON (%s); keeping raw text", exc)
            assessments, summary = (), ""
        return BlockAnalysis(
            analysis_id=str(uuid.uuid4()),
            assessments=assessments,
            summary_explanation=summary,
            raw_text=raw_text
        )

    def _complete(self, request):
        role = getattr(self.sampling, request.role)
        request = replace(request, temperature=role.temperature, top_p=role.top_p,
                          max_output_tokens=role.max_output_tokens,
                          seed=(self.seed + self.budget.usage.total_model_calls if self.seed is not None and self.budget else self.seed))
        response = complete_request(self.gateway, request, self.budget)
        if self.require_exact_token_count and (response.prompt_tokens is None or response.completion_tokens is None):
            from rethink_mcts.domain.errors import ModelError
            raise ModelError("Provider did not supply required token usage")
        return response

    def repair(self, statement, execution_spec, candidate_code, feedback):
        prompt = self._render("repair_code.jinja",
            statement=statement, candidate_code=candidate_code,
            feedback_text=feedback.format_as_text(), **interface_context(execution_spec))
        response = self._complete(GenerationRequest(
            request_id=f"req_repair_{uuid.uuid4().hex[:8]}", role="code", prompt=prompt))
        return extract_python_code(response.content)
