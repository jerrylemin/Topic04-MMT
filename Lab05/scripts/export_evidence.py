"""Run the fixed Flask flows and export redacted evidence from real handlers/SQLite."""

import json
import re
import secrets
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402
from config import AUTH_LOGIC_INPUT, Config, QUOTE_INPUT, SEARCH_EXPANDED_INPUT  # noqa: E402
from database import query_all  # noqa: E402
from seed import reset_database  # noqa: E402
from trace_service import get_trace  # noqa: E402


TRACE_NAMES = (
    "normal_login_vulnerable",
    "quote_login_vulnerable",
    "auth_logic_vulnerable",
    "auth_logic_secure",
    "normal_login_secure",
    "normal_search_vulnerable",
    "quote_search_vulnerable",
    "expanded_search_vulnerable",
    "expanded_search_secure",
    "normal_search_secure",
    "user_detail_vulnerable",
    "user_detail_secure",
)
REQUEST_RESPONSE_NAMES = TRACE_NAMES[:10]
DEMO_PASSWORDS = ("AdminLab123!", "StudentA123!", "StudentB123!")
FULL_DIGEST = re.compile(r"\b[a-f0-9]{64}\b", re.IGNORECASE)


def _write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def _request_text(trace: dict) -> str:
    item = trace["request_inspector"]
    return "\n".join((
        f"Method: {item.get('method')}",
        f"Full URL: {item.get('full_url')}",
        f"Path: {item.get('path')}",
        f"Query string: {item.get('query_string') or '-'}",
        f"Content-Type: {item.get('content_type') or '-'}",
        f"Content-Length: {item.get('content_length', 0)}",
        f"Form field names: {json.dumps(item.get('form_field_names', []), ensure_ascii=False)}",
        f"Form values: {json.dumps(item.get('form_values', {}), ensure_ascii=False)}",
        f"Session present: {item.get('session_present')}",
        f"Route handler: {item.get('route_handler')}",
        f"Timestamp: {item.get('timestamp') or trace.get('timestamp')}",
    )) + "\n"


def _response_text(response, trace: dict) -> str:
    verdict = trace.get("final_verdict", {})
    execution = trace.get("execution_inspector", {})
    return "\n".join((
        f"HTTP status: {response.status_code}",
        f"Content-Type: {response.headers.get('Content-Type', '-')}",
        f"Content-Security-Policy: {response.headers.get('Content-Security-Policy', '-')}",
        f"Trace ID: {trace['trace_id']}",
        f"Decision: {response.headers.get('X-Lab-Decision', verdict.get('final_decision', '-'))}",
        f"Result count: {response.headers.get('X-Lab-Result-Count', execution.get('rows_returned', 0))}",
        f"Error category: {response.headers.get('X-Lab-Error-Category', execution.get('error_category') or 'none')}",
        f"Prepared statement: {response.headers.get('X-Lab-Prepared', verdict.get('prepared_statement_used', False))}",
    )) + "\n"


def _assert_redacted(value) -> None:
    text = json.dumps(value, ensure_ascii=False)
    if any(password in text for password in DEMO_PASSWORDS) or FULL_DIGEST.search(text):
        raise RuntimeError("Evidence contains a plaintext demo password or full digest/hash.")


def run_fixed_flows() -> tuple[dict, dict]:
    app = create_app({
        "TESTING": True,
        "DATABASE": Config.DATABASE,
        "SERVER_NAME": "127.0.0.1:5005",
        "SECRET_KEY": secrets.token_hex(32),
    })
    with app.app_context():
        reset_database()
    client = app.test_client()
    captured: dict[str, tuple] = {}

    def run(name: str, method: str, path: str, **kwargs):
        response = getattr(client, method)(path, **kwargs)
        trace_id = response.headers.get("X-Lab-Trace-ID")
        if not trace_id:
            raise RuntimeError(f"Flow {name} did not return a trace ID.")
        with app.app_context():
            trace = get_trace(trace_id)
        if not trace:
            raise RuntimeError(f"Flow {name} trace {trace_id} was not persisted.")
        captured[name] = (response, trace)

    run("normal_login_vulnerable", "post", "/vulnerable/login", data={"username": "admin_lab", "password": "AdminLab123!"})
    client.post("/logout")
    run("quote_login_vulnerable", "post", "/vulnerable/login", data={"username": QUOTE_INPUT, "password": "x"})
    run("auth_logic_vulnerable", "post", "/vulnerable/login", data={"username": AUTH_LOGIC_INPUT, "password": "wrong-local-demo"})
    client.post("/logout")
    run("auth_logic_secure", "post", "/secure/login", data={"username": AUTH_LOGIC_INPUT, "password": "wrong-local-demo"})
    run("normal_login_secure", "post", "/secure/login", data={"username": "admin_lab", "password": "AdminLab123!"})
    client.post("/logout")
    run("normal_search_vulnerable", "get", "/vulnerable/search", query_string={"keyword": "USB"})
    run("quote_search_vulnerable", "get", "/vulnerable/search", query_string={"keyword": QUOTE_INPUT})
    run("expanded_search_vulnerable", "get", "/vulnerable/search", query_string={"keyword": SEARCH_EXPANDED_INPUT})
    run("expanded_search_secure", "get", "/secure/search", query_string={"keyword": SEARCH_EXPANDED_INPUT})
    run("normal_search_secure", "get", "/secure/search", query_string={"keyword": "USB"})
    run("user_detail_vulnerable", "get", "/vulnerable/user", query_string={"id": "1"})
    run("user_detail_secure", "get", "/secure/user", query_string={"id": "1"})

    with app.app_context():
        audit_rows = [dict(row) for row in query_all("SELECT * FROM audit_logs ORDER BY id")]
        query_rows = [dict(row) for row in query_all("SELECT * FROM query_events ORDER BY id")]
        login_rows = [dict(row) for row in query_all("SELECT * FROM login_attempts ORDER BY id")]
        counts = {
            table: len(query_all(f"SELECT id FROM {table}"))
            for table in ("users", "products", "audit_logs", "login_attempts", "query_events")
        }
    state = {"audit_logs": audit_rows, "query_events": query_rows, "login_attempts": login_rows, "counts": counts}
    _assert_redacted({name: trace for name, (_response, trace) in captured.items()})
    _assert_redacted(state)
    return captured, state


def export_evidence() -> dict:
    captured, state = run_fixed_flows()
    for name in TRACE_NAMES:
        _write_json(ROOT / "evidence" / "traces" / f"{name}.json", captured[name][1])
    for name in REQUEST_RESPONSE_NAMES:
        response, trace = captured[name]
        _write_text(ROOT / "evidence" / "requests" / f"{name}.txt", _request_text(trace))
        _write_text(ROOT / "evidence" / "responses" / f"{name}.txt", _response_text(response, trace))

    query_groups = {
        "vulnerable_login_queries.json": ("vulnerable", "login"),
        "secure_login_queries.json": ("secure", "login"),
        "vulnerable_search_queries.json": ("vulnerable", "search"),
        "secure_search_queries.json": ("secure", "search"),
    }
    for filename, (mode, feature) in query_groups.items():
        records = []
        for row in state["query_events"]:
            if row["mode"] != mode or row["feature"] != feature:
                continue
            records.append({
                "query_template": row["query_template"],
                "construction_type": "parameter_binding" if mode == "secure" else "string_concatenation",
                "final_query_masked": row["final_query_masked"],
                "parameters_masked": json.loads(row["parameters_json"]),
                "rows_returned": row["result_count"],
                "error_category": row["error_category"],
                "trace_id": row["trace_id"],
            })
        _write_json(ROOT / "evidence" / "queries" / filename, records)

    _write_json(ROOT / "evidence" / "audit" / "audit_logs.json", state["audit_logs"])
    _write_json(ROOT / "evidence" / "results" / "flow_results.json", {
        name: captured[name][1]["final_verdict"] for name in TRACE_NAMES
    })
    _write_json(ROOT / "evidence" / "errors" / "handled_errors.json", {
        name: captured[name][1].get("error_inspector")
        for name in TRACE_NAMES if captured[name][1].get("error_inspector")
    })
    _write_json(ROOT / "evidence" / "database" / "database_snapshot.json", {
        "database": "Lab05 local SQLite", "counts": state["counts"], "read_only_demo_flows": True
    })
    _assert_redacted(state)
    return {"flows": len(captured), "audit_events": len(state["audit_logs"]), "query_events": len(state["query_events"])}


def main() -> int:
    summary = export_evidence()
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
