"""
SemanticPromptedLLM implementing semantic model ports using Jinja2 templates and ModelGateway.
"""

import os
import uuid
from dataclasses import replace
from rethink_mcts.config import SamplingConfig
from rethink_mcts.application.model_calls import complete_request
from typing import Optional
from jinja2 import Environment, FileSystemLoader

from rethink_mcts.domain.problem import ExecutionSpec
from rethink_mcts.domain.tree import ProposalBatch, ThoughtProposal
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


class SemanticPromptedLLM(
    ThoughtProposer,
    CodeGenerator,
    ThoughtRefiner,
    CodeCritic,
    BlockAnalyzer
):
    """
    Renders prompts from Jinja2 templates, calls ModelGateway, and parses structured output.
    """
    def __init__(
        self,
        gateway: ModelGateway,
        prompts_dir: str = "prompts/compact_v1",
        prior_policy: Optional[PriorPolicy] = None,
        sampling=None, seed=None, critic_min=0.0, critic_max=1.0, max_prompt_blocks=32, require_exact_token_count=False
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

        self.env = Environment(loader=FileSystemLoader(self.prompts_dir))

    def propose(
        self,
        statement: str,
        active_thoughts: tuple[str, ...],
        width: int,
        feedback: Optional[VerbalFeedback] = None
    ) -> ProposalBatch:
        template = self.env.get_template("expand.jinja")
        prompt = template.render(
            statement=statement,
            active_thoughts=list(active_thoughts),
            width=width,
            feedback_text=feedback.format_as_text() if feedback else ""
        )

        req = GenerationRequest(
            request_id=f"req_exp_{uuid.uuid4().hex[:8]}",
            role="expansion",
            prompt=prompt,
            temperature=0.6,
            max_output_tokens=384,
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
        template = self.env.get_template("generate_code.jinja")
        prompt = template.render(
            statement=statement,
            active_thoughts=list(active_thoughts),
            mode=execution_spec.mode.value if hasattr(execution_spec.mode, "value") else str(execution_spec.mode),
            entry_point=execution_spec.entry_point or "solution",
            public_examples=public_examples_str
        )

        req = GenerationRequest(
            request_id=f"req_gen_{uuid.uuid4().hex[:8]}",
            role="code",
            prompt=prompt,
            temperature=0.2,
            max_output_tokens=1536
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
        template = self.env.get_template("rethink.jinja")
        prompt = template.render(
            statement=statement,
            parent_thoughts=list(parent_thoughts),
            erroneous_thought=erroneous_thought,
            candidate_code=candidate_code,
            feedback_text=feedback.format_as_text()
        )

        req = GenerationRequest(
            request_id=f"req_reth_{uuid.uuid4().hex[:8]}",
            role="rethink",
            prompt=prompt,
            temperature=0.3,
            max_output_tokens=256
        )
        resp = self._complete(req)
        return resp.content.strip()

    def assess(
        self,
        statement: str,
        candidate_code: str
    ) -> float:
        template = self.env.get_template("self_eval.jinja")
        prompt = template.render(
            statement=statement,
            candidate_code=candidate_code,
            score_min=self.critic_min,
            score_max=self.critic_max
        )

        req = GenerationRequest(
            request_id=f"req_crit_{uuid.uuid4().hex[:8]}",
            role="critic",
            prompt=prompt,
            temperature=0.0,
            max_output_tokens=64,
            response_contract="json"
        )
        resp = self._complete(req)
        return parse_critic_score(resp.content, score_min=self.critic_min, score_max=self.critic_max)

    def analyze(
        self,
        statement: str,
        candidate_code: str,
        facts: ExecutionFacts,
        trace: TraceResult
    ) -> BlockAnalysis:
        template = self.env.get_template("analyze_block.jinja")
        trace_snippets = []
        for v in trace.block_visits[:self.max_prompt_blocks]:
            before_str = ", ".join(f"{k}={val}" for k, val in v.locals_before.items()) if v.locals_before else "none"
            after_str = ", ".join(f"{k}={val}" for k, val in v.locals_after.items()) if v.locals_after else "none"
            exit_note = f" (exit: {v.exit_kind})" if v.exit_kind and v.exit_kind != "fallthrough" else ""
            trace_snippets.append(
                f"[{v.block_id}{exit_note}]\n# Locals before: {before_str}\n{v.source_snippet.strip()}\n# Locals after: {after_str}"
            )

        prompt = template.render(
            statement=statement,
            candidate_code=candidate_code,
            facts_text=f"{facts.failure_kind}: expected {facts.expected_output_snippet}, got {facts.actual_output_snippet}",
            trace_text="\n\n".join(trace_snippets)
        )

        req = GenerationRequest(
            request_id=f"req_anlz_{uuid.uuid4().hex[:8]}",
            role="block_analysis",
            prompt=prompt,
            temperature=0.0,
            max_output_tokens=512,
            response_contract="json"
        )
        resp = self._complete(req)
        # Parse JSON structure
        try:
            import json
            import re
            cleaned = resp.content.strip()
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
            if match:
                cleaned = match.group(1).strip()
            elif cleaned.startswith("```"):
                lines = cleaned.splitlines()
                if lines and lines[0].strip().startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip().startswith("```"):
                    lines = lines[:-1]
                cleaned = "\n".join(lines).strip()
            data = json.loads(cleaned)

            raw_items = []
            summary = ""
            if isinstance(data, list):
                raw_items = data
            elif isinstance(data, dict):
                summary = str(data.get("summary", ""))
                raw_items = data.get("assessments", data.get("blocks", data.get("analysis", [])))

            assessments = []
            for item in raw_items:
                if not isinstance(item, dict):
                    continue
                bid = str(item.get("block_id", item.get("block", "")))
                if "correct" in item:
                    c_val = item["correct"]
                    if isinstance(c_val, bool):
                        verdict = BlockVerdict.CORRECT if c_val else BlockVerdict.INCORRECT
                    else:
                        c_str = str(c_val).strip().lower()
                        verdict = BlockVerdict.CORRECT if c_str in ("true", "1", "yes") else (BlockVerdict.INCORRECT if c_str in ("false", "0", "no") else BlockVerdict.UNKNOWN)
                else:
                    v_str = str(item.get("verdict", "unknown")).strip().lower()
                    verdict = BlockVerdict.CORRECT if v_str == "correct" else (BlockVerdict.INCORRECT if v_str == "incorrect" else BlockVerdict.UNKNOWN)
                expl = str(item.get("explanation", item.get("reason", "")))
                assessments.append(BlockAssessment(block_id=bid, verdict=verdict, explanation=expl))

            return BlockAnalysis(
                analysis_id=str(uuid.uuid4()),
                assessments=tuple(assessments),
                summary_explanation=summary
            )
        except Exception as exc:
            import logging
            logging.getLogger(__name__).warning("Failed to parse block analysis output: %s. Raw: %r", exc, resp.content)
            return BlockAnalysis(
                analysis_id=str(uuid.uuid4()),
                assessments=(),
                summary_explanation=f"Failed to parse block analysis output: {exc}"
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
        prompt = self.env.get_template("repair_code.jinja").render(
            statement=statement, candidate_code=candidate_code,
            feedback_text=feedback.format_as_text(), entry_point=execution_spec.entry_point)
        response = self._complete(GenerationRequest(
            request_id=f"req_repair_{uuid.uuid4().hex[:8]}", role="code", prompt=prompt))
        return extract_python_code(response.content)
