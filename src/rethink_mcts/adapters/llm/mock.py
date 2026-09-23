"""
Deterministic Scenario Mock implementing semantic model ports for testing and M1 verification.
Does NOT use global mutable flags (matching §18.3).
"""

import uuid
from typing import List, Optional
from rethink_mcts.domain.tree import ThoughtProposal, ProposalBatch
from rethink_mcts.domain.problem import ExecutionSpec
from rethink_mcts.domain.feedback import ExecutionFacts, TraceResult, BlockAnalysis, BlockAssessment, BlockVerdict, VerbalFeedback
from rethink_mcts.ports.models import (
    GenerationRequest,
    GenerationResponse,
    ModelGateway,
    ThoughtProposer,
    CodeGenerator,
    ThoughtRefiner,
    CodeCritic,
    BlockAnalyzer
)


class ScenarioMockLLM(
    ModelGateway,
    ThoughtProposer,
    CodeGenerator,
    ThoughtRefiner,
    CodeCritic,
    BlockAnalyzer
):
    """
    Deterministic mock supporting Scenario A (Watermelon), Scenario B, and arbitrary tests.
    """
    def __init__(self, default_critic_score: float = 0.9):
        self.default_critic_score = default_critic_score
        self.propose_calls = 0
        self.generate_calls = 0
        self.refine_calls = 0
        self.critic_calls = 0
        self.analyze_calls = 0

    def propose(
        self,
        statement: str,
        active_thoughts: tuple[str, ...],
        width: int,
        feedback: Optional[VerbalFeedback] = None
    ) -> ProposalBatch:
        self.propose_calls += 1
        proposals: List[ThoughtProposal] = []

        if not active_thoughts:
            # Root expansion
            raw = [
                ("Check parity directly: check if number is simply even by w % 2 == 0", 0.7),
                ("Exhaustive check: find two positive even integers that sum to w", 0.3)
            ][:width]
        else:
            # Child expansion
            prefix = " -> ".join(active_thoughts)
            raw = [
                (f"Refinement of [{prefix}]: verify constraints and boundary cases", 0.8),
                (f"Alternative from [{prefix}]: optimize edge case branches", 0.2)
            ][:width]

        total = sum(s for _, s in raw)
        proposals = [
            ThoughtProposal(
                text=t,
                raw_reasonableness=s,
                normalized_prior=s / total
            )
            for t, s in raw
        ]
        return ProposalBatch(batch_id=str(uuid.uuid4()), proposals=tuple(proposals))

    def generate(
        self,
        statement: str,
        execution_spec: ExecutionSpec,
        active_thoughts: tuple[str, ...],
        public_examples_str: str = ""
    ) -> str:
        self.generate_calls += 1
        path_str = " ".join(active_thoughts).lower()

        # If thought mentions w > 2 or positive even division, generate correct code
        if "w > 2" in path_str or "positive even" in path_str or "each part must be a positive even" in path_str:
            return "w = int(input())\nif w % 2 == 0 and w > 2:\n    print('YES')\nelse:\n    print('NO')\n"

        # Default naive watermelon code (fails on w=2)
        if "watermelon" in statement.lower() or "w % 2 == 0" in path_str or "parity" in path_str:
            return "w = int(input())\nif w % 2 == 0:\n    print('YES')\nelse:\n    print('NO')\n"

        # Generic function or stdin code
        if execution_spec.entry_point:
            return f"def {execution_spec.entry_point}(*args, **kwargs):\n    return True\n"
        return "print('YES')\n"

    def refine(
        self,
        statement: str,
        execution_spec: ExecutionSpec,
        parent_thoughts: tuple[str, ...],
        erroneous_thought: str,
        candidate_code: str,
        feedback: VerbalFeedback
    ) -> str:
        self.refine_calls += 1
        # Scenario A resolution:
        return (
            "Rethink Strategy: While w must be even, each part must be a positive even integer (>= 2). "
            "Thus w=2 cannot be divided into two positive evens. We must check w % 2 == 0 and w > 2."
        )

    def assess(
        self,
        statement: str,
        candidate_code: str
    ) -> float:
        self.critic_calls += 1
        return self.default_critic_score

    def analyze(
        self,
        statement: str,
        candidate_code: str,
        facts: ExecutionFacts,
        trace: TraceResult
    ) -> BlockAnalysis:
        self.analyze_calls += 1
        assessments = []
        if trace and trace.block_visits:
            for v in trace.block_visits:
                # If block has conditional check w % 2 == 0 without w > 2, flag it as incorrect
                if "% 2" in v.source_snippet and "> 2" not in v.source_snippet:
                    assessments.append(
                        BlockAssessment(
                            block_id=v.block_id,
                            verdict=BlockVerdict.INCORRECT,
                            explanation="Condition checks parity only, failing for w=2 where 2 cannot be split into positive evens."
                        )
                    )
                else:
                    assessments.append(
                        BlockAssessment(
                            block_id=v.block_id,
                            verdict=BlockVerdict.CORRECT,
                            explanation="Block execution matches expected behavior."
                        )
                    )
        return BlockAnalysis(
            analysis_id=str(uuid.uuid4()),
            assessments=tuple(assessments),
            summary_explanation="Identified edge-case logical fault in condition check."
        )

    def complete(self, request: GenerationRequest) -> GenerationResponse:
        content = "def solution(*args, **kwargs):\n    return True\n"
        if "analyze" in request.role or "analysis" in request.role:
            content = "1. Constraints: integer inputs\n2. Edge cases: negative, zero\n3. Pitfalls: off-by-one"
        elif "draft" in request.role:
            content = "### Strategy A\n```python\nprint('YES')\n```\n\n### Strategy B\n```python\nprint('YES')\n```"
        elif "code" in request.role:
            content = "```python\nw = int(input())\nif w % 2 == 0 and w > 2:\n    print('YES')\nelse:\n    print('NO')\n```"
        return GenerationResponse(content=content, finish_reason="stop")

