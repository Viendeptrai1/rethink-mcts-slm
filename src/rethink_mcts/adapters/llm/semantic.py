"""
SemanticPromptedLLM implementing semantic model ports using Jinja2 templates and ModelGateway.
"""

import os
import uuid
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
        prior_policy: Optional[PriorPolicy] = None
    ):
        self.gateway = gateway
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
            width=width
        )

        req = GenerationRequest(
            request_id=f"req_exp_{uuid.uuid4().hex[:8]}",
            role="expansion",
            prompt=prompt,
            temperature=0.6,
            max_output_tokens=384,
            response_contract="json"
        )
        resp = self.gateway.complete(req)

        raw_proposals = parse_thoughts_json(resp.content)
        processed = self.prior_policy.process_raw_proposals(raw_proposals)

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
        resp = self.gateway.complete(req)
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
        resp = self.gateway.complete(req)
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
            score_min=0.0,
            score_max=1.0
        )

        req = GenerationRequest(
            request_id=f"req_crit_{uuid.uuid4().hex[:8]}",
            role="critic",
            prompt=prompt,
            temperature=0.0,
            max_output_tokens=64,
            response_contract="json"
        )
        resp = self.gateway.complete(req)
        return parse_critic_score(resp.content, score_min=0.0, score_max=1.0)

    def analyze(
        self,
        statement: str,
        candidate_code: str,
        facts: ExecutionFacts,
        trace: TraceResult
    ) -> BlockAnalysis:
        template = self.env.get_template("analyze_block.jinja")
        trace_snippets = []
        for v in trace.block_visits[:16]:
            trace_snippets.append(f"Block {v.block_id}: {v.source_snippet.strip()}")

        prompt = template.render(
            statement=statement,
            candidate_code=candidate_code,
            facts_text=f"{facts.failure_kind}: expected {facts.expected_output_snippet}, got {facts.actual_output_snippet}",
            trace_text="\n".join(trace_snippets)
        )

        req = GenerationRequest(
            request_id=f"req_anlz_{uuid.uuid4().hex[:8]}",
            role="block_analysis",
            prompt=prompt,
            temperature=0.0,
            max_output_tokens=512,
            response_contract="json"
        )
        resp = self.gateway.complete(req)
        # Parse JSON structure
        try:
            import json
            cleaned = resp.content.strip()
            if cleaned.startswith("```"):
                lines = cleaned.splitlines()
                cleaned = "\n".join(lines[1:-1]).strip()
            data = json.loads(cleaned)
            assessments = []
            for item in data.get("assessments", []):
                v_str = str(item.get("verdict", "unknown")).lower()
                verdict = BlockVerdict.CORRECT if v_str == "correct" else (BlockVerdict.INCORRECT if v_str == "incorrect" else BlockVerdict.UNKNOWN)
                assessments.append(
                    BlockAssessment(
                        block_id=str(item.get("block_id", "")),
                        verdict=verdict,
                        explanation=str(item.get("explanation", ""))
                    )
                )
            return BlockAnalysis(
                analysis_id=str(uuid.uuid4()),
                assessments=tuple(assessments),
                summary_explanation=str(data.get("summary", ""))
            )
        except Exception:
            return BlockAnalysis(
                analysis_id=str(uuid.uuid4()),
                assessments=(),
                summary_explanation="Failed to parse block analysis output"
            )
