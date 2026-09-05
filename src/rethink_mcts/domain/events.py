"""
Event envelopes and transaction semantics for search persistence and auditing.
"""

import time
import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class EventEnvelope:
    schema_version: int
    event_id: str
    sequence: int
    run_id: str
    problem_id: str
    timestamp: float
    event_type: str
    payload: dict

    @classmethod
    def create(
        cls,
        sequence: int,
        run_id: str,
        problem_id: str,
        event_type: str,
        payload: dict
    ) -> "EventEnvelope":
        return cls(
            schema_version=1,
            event_id=str(uuid.uuid4()),
            sequence=sequence,
            run_id=run_id,
            problem_id=problem_id,
            timestamp=time.time(),
            event_type=event_type,
            payload=payload
        )
