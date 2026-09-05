"""
Execution facts, bytecode CFG, dynamic trace visits, and verbal feedback contracts.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


@dataclass(frozen=True)
class ExecutionFacts:
    failure_kind: str
    input_snippet: str
    expected_output_snippet: str
    actual_output_snippet: str
    traceback_snippet: Optional[str] = None
    public_passed: int = 0
    public_total: int = 0


@dataclass(frozen=True)
class BlockVisit:
    visit_id: str
    block_id: str
    frame_id: str
    sequence_number: int
    line_span: tuple[int, int]
    source_snippet: str
    locals_before: dict[str, str] = field(default_factory=dict)
    locals_after: dict[str, str] = field(default_factory=dict)
    exit_kind: str = "fallthrough"  # fallthrough | jump | return | exception
    exception_type: Optional[str] = None
    truncated: bool = False


@dataclass(frozen=True)
class TraceResult:
    status: str  # "success" | "degraded" | "timeout" | "unsupported"
    block_visits: tuple[BlockVisit, ...] = field(default_factory=tuple)
    omitted_visits_count: int = 0
    degraded_reason: Optional[str] = None


class BlockVerdict(str, Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class BlockAssessment:
    block_id: str
    verdict: BlockVerdict
    explanation: str


@dataclass(frozen=True)
class BlockAnalysis:
    analysis_id: str
    assessments: tuple[BlockAssessment, ...] = field(default_factory=tuple)
    summary_explanation: str = ""


@dataclass(frozen=True)
class VerbalFeedback:
    feedback_id: str
    candidate_id: str
    facts: ExecutionFacts
    trace: Optional[TraceResult] = None
    analysis: Optional[BlockAnalysis] = None

    def format_as_text(self) -> str:
        """Render structured verbal feedback to text for inclusion in prompts."""
        parts = [
            f"[EXECUTION REPORT]",
            f"Result: {self.facts.failure_kind} ({self.facts.public_passed}/{self.facts.public_total} passed)",
            f"Input:\n{self.facts.input_snippet}",
            f"Expected Output:\n{self.facts.expected_output_snippet}",
            f"Actual Output:\n{self.facts.actual_output_snippet}"
        ]
        if self.facts.traceback_snippet:
            parts.append(f"Traceback:\n{self.facts.traceback_snippet}")

        if self.trace and self.trace.block_visits:
            trace_parts = ["[EXECUTION TRACE (BASIC BLOCKS)]"]
            for v in self.trace.block_visits[:16]:  # Bounded presentation
                delta = []
                for k, val in v.locals_after.items():
                    if v.locals_before.get(k) != val:
                        delta.append(f"{k}: {v.locals_before.get(k, '<none>')} -> {val}")
                delta_str = ", ".join(delta) if delta else "no changes"
                trace_parts.append(
                    f"Block {v.block_id} (lines {v.line_span[0]}-{v.line_span[1]}): {v.source_snippet.strip()} | Vars: [{delta_str}]"
                )
            if self.trace.omitted_visits_count > 0:
                trace_parts.append(f"... ({self.trace.omitted_visits_count} loop visits omitted)")
            parts.append("\n".join(trace_parts))

        if self.analysis and self.analysis.assessments:
            analysis_parts = ["[BLOCK ANALYSIS]"]
            for a in self.analysis.assessments:
                analysis_parts.append(f"Block {a.block_id}: {a.verdict.value.upper()} - {a.explanation}")
            if self.analysis.summary_explanation:
                analysis_parts.append(f"Summary: {self.analysis.summary_explanation}")
            parts.append("\n".join(analysis_parts))

        return "\n\n".join(parts)
