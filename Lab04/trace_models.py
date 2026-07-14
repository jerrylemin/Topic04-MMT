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
    technique: str = ""
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
    lab_type: str = "CSRF"
    mode: str = "informational"
    action: str = "request"
    current_user: str | None = None
    attacker_origin: str | None = None
    victim_origin: str = "http://127.0.0.1:5004"
    same_origin: bool | None = None
    same_site: bool | None = None
    request_method: str = "GET"
    full_url: str = ""
    path: str = ""
    query_string: str = ""
    content_type: str | None = None
    content_length: int = 0
    form_field_names: list[str] = field(default_factory=list)
    form_values: dict = field(default_factory=dict)
    host: str = ""
    route_handler: str = ""
    cookie_present: bool = False
    origin_header: str | None = None
    referer_header: str | None = None
    parsed_scheme: str | None = None
    parsed_hostname: str | None = None
    parsed_port: int | None = None
    expected_origins: list[str] = field(default_factory=list)
    origin_match: bool | None = None
    referer_match: bool | None = None
    csrf_token_present: bool = False
    csrf_token_status: str = "not_required"
    origin_decision: str = "not_checked"
    reauthentication_status: str = "not_required"
    state_before: dict = field(default_factory=dict)
    state_after: dict = field(default_factory=dict)
    http_status: int = 200
    final_result: str = "request_received"
    request_sent: bool = True
    response_readable_by_attacker: bool = False
    steps: list[TraceStep | dict] = field(default_factory=list)
    timestamp: str = field(default_factory=utc_now)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["origin"] = self.origin_header
        data["referer"] = self.referer_header
        return data
