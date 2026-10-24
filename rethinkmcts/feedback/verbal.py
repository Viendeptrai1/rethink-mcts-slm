from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from ..parsing import parse_feedback
from ..prompts import feedback_prompt
from .trace import TraceResult, format_trace


@dataclass(frozen=True)
class FeedbackBundle:
    failed_test: str
    trace: TraceResult
    trace_text: str
    analysis: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "failed_test": self.failed_test,
            "trace_text": self.trace_text,
            "analysis": self.analysis,
            "trace_status": self.trace.status,
            "trace_error": self.trace.error,
        }


def build_feedback(
    *,
    statement: str,
    thoughts: list[str],
    code: str,
    failed_test: str,
    trace: TraceResult,
    analyze: Callable[[str], str],
    max_blocks: int = 10,
    max_block_chars: int = 5000,
    max_feedback_chars: int = 8000,
) -> FeedbackBundle:
    trace_text = format_trace(trace, max_blocks=max_blocks, max_chars=max_block_chars)
    prompt = feedback_prompt(statement, thoughts, code, failed_test, trace_text)
    response = analyze(prompt)
    analysis = parse_feedback(response)
    combined = (trace_text + "\n\nAnalysis:\n" + response).strip()
    if len(combined) > max_feedback_chars:
        combined = combined[:max_feedback_chars]
    return FeedbackBundle(
        failed_test=failed_test,
        trace=trace,
        trace_text=combined,
        analysis=analysis,
    )
