from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class TraceStep:
    step_number: int
    layer: str
    title: str
    description: str
    technique: str
    input_data: dict = field(default_factory=dict)
    output_data: dict = field(default_factory=dict)
    code_reference: str = ""
    security_meaning: str = ""
    status: str = "observed"
    timestamp: str = field(default_factory=utc_now)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RequestTrace:
    trace_id: str
    mode: str
    feature: str
    request_inspector: dict
    input_inspector: dict
    query_inspector: dict
    execution_inspector: dict
    decision_inspector: dict
    database_inspector: dict
    error_inspector: dict | None
    final_verdict: dict
    steps: list[TraceStep | dict]
    timestamp: str = field(default_factory=utc_now)

    def to_dict(self) -> dict:
        return asdict(self)

