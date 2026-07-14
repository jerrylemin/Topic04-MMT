from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from security_utils import redact


@dataclass(frozen=True, slots=True)
class TraceStep:
    step_number: int
    timestamp: str
    layer: str
    title: str
    description: str
    technique: str
    input_data: Any
    output_data: Any
    code_reference: str
    security_meaning: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        return redact(asdict(self))


@dataclass(frozen=True, slots=True)
class FinalVerdict:
    mode: str
    cookie_name: str | None
    cookie_source: str
    role_source: str
    integrity_protected: bool
    confidentiality_protected: bool
    server_session_used: bool
    cookie_modified: bool
    modification_detected: bool
    database_role_checked: bool
    authorization_decision: str
    access_granted: bool
    audit_event: str
    root_cause: str
    primary_fix: str
    defense_in_depth: str
    remaining_risk: str

    def to_dict(self) -> dict[str, Any]:
        return redact(asdict(self))


@dataclass(slots=True)
class TraceRecord:
    trace_id: str
    mode: str
    route: str
    started_at: str
    status: str = "in_progress"
    completed_at: str | None = None
    steps: list[TraceStep] = field(default_factory=list)
    verdict: FinalVerdict | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "mode": self.mode,
            "route": self.route,
            "started_at": self.started_at,
            "status": self.status,
            "completed_at": self.completed_at,
            "steps": [step.to_dict() for step in self.steps],
            "verdict": None if self.verdict is None else self.verdict.to_dict(),
        }
