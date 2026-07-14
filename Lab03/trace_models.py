from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


@dataclass
class TraceStep:
    step_number: int
    layer: str
    title: str
    description: str
    technique: str = ""
    input_data: object = ""
    output_data: object = ""
    code_reference: str = ""
    security_meaning: str = ""
    status: str = "normal"
    timestamp: str = field(default_factory=now)


@dataclass
class Trace:
    trace_id: str
    scenario: str
    mode: str
    current_user: dict
    request_inspector: dict
    steps: list[TraceStep] = field(default_factory=list)
    database_inspector: dict = field(default_factory=dict)
    authorization_inspector: dict = field(default_factory=dict)
    parameter_diff: list[dict] = field(default_factory=list)
    final_verdict: dict = field(default_factory=dict)
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict:
        payload = asdict(self)
        database = payload["database_inspector"]
        verdict = payload["final_verdict"]
        authorization = payload["authorization_inspector"]
        if self.scenario == "checkout":
            payload.update({
                "product_id": database.get("product_id"), "quantity": database.get("quantity"),
                "database_price": database.get("database_price"), "submitted_price": database.get("submitted_price"),
                "calculated_total": database.get("stored_total"), "stored_total": database.get("stored_total"),
                "price_mismatch": database.get("database_price") != database.get("submitted_price"),
                "decision": "accepted" if self.mode == "vulnerable" else "client price ignored",
                "audit_event": verdict.get("audit_event"),
            })
        elif self.scenario == "invoice":
            payload.update({
                "current_user_id": self.current_user.get("user_id"), "invoice_id": database.get("invoice_id"),
                "invoice_owner_id": database.get("owner_id"), "ownership_match": database.get("ownership_match"),
                "authorization_policy": authorization.get("policy", "none"),
                "decision": authorization.get("decision", "not checked"), "http_status": verdict.get("http_status", 200),
                "data_returned": verdict.get("unauthorized_resource_disclosed", False) or self.mode == "vulnerable",
            })
        elif self.scenario == "profile":
            payload.update({
                "current_user_id": database.get("current_user_id_from_session"),
                "submitted_user_id": database.get("target_user_id_from_form"),
                "submitted_role": database.get("submitted_role"), "accepted_fields": database.get("accepted_fields", []),
                "rejected_fields": database.get("rejected_fields", []), "role_before": database.get("role_before"),
                "role_after": database.get("role_after"), "decision": authorization.get("decision", "not checked"),
                "audit_event": verdict.get("audit_event"),
            })
        return payload
