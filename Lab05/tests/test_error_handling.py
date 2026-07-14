import json
import re
import sqlite3

from config import QUOTE_INPUT
from error_service import categorize_database_error, error_inspector


WINDOWS_ABSOLUTE_PATH = re.compile(r"[A-Za-z]:[\\/]")


def _quote_trace(client, feature):
    if feature == "login":
        response = client.post("/vulnerable/login", data={"username": QUOTE_INPUT, "password": "x"})
    else:
        response = client.get("/vulnerable/search", query_string={"keyword": QUOTE_INPUT})
    return response, client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()


def test_vulnerable_error_is_categorized_without_traceback(shared_client):
    response, trace = _quote_trace(shared_client, "login")
    error = trace["error_inspector"]
    assert error["category"] == "sql_syntax_error"
    assert error["exception_class"] == "OperationalError"
    assert error["handled"] is True
    assert b"Traceback" not in response.data


def test_vulnerable_error_explains_root_cause_and_insertion_point(shared_client):
    _, trace = _quote_trace(shared_client, "search")
    error = trace["error_inspector"]
    assert error["input_insertion"] == "keyword_inside_like_pattern"
    assert "concatenated" in error["root_cause"]
    assert error["data_modified"] is False


def test_error_inspector_does_not_expose_absolute_path_or_full_digest(shared_client):
    _, trace = _quote_trace(shared_client, "login")
    serialized = json.dumps(trace["error_inspector"])
    assert not WINDOWS_ABSOLUTE_PATH.search(serialized)
    assert not re.search(r"\b[a-f0-9]{64}\b", serialized, re.IGNORECASE)


def test_secure_sql_shaped_inputs_do_not_create_error_inspector(shared_client):
    response = shared_client.get("/secure/search", query_string={"keyword": QUOTE_INPUT})
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    assert trace["error_inspector"] is None
    assert trace["execution_inspector"]["error_category"] is None


def test_unknown_trace_returns_generic_json_404(shared_client):
    response = shared_client.get("/api/trace/not-a-real-trace")
    assert response.status_code == 404
    assert response.get_json() == {"error": "trace not found"}


def test_error_categorizer_handles_no_error():
    assert categorize_database_error(None) is None


def test_error_categorizer_handles_generic_database_failure():
    assert categorize_database_error(sqlite3.DatabaseError("database unavailable")) == "database_error"


def test_error_categorizer_handles_non_database_failure():
    assert categorize_database_error(RuntimeError("unexpected local failure")) == "internal_error"


def test_secure_error_inspector_returns_only_generic_safe_fields():
    info = error_inspector(sqlite3.DatabaseError("C:\\private\\lab05.sqlite3 failed"), secure=True)
    assert info["category"] == "database_error"
    assert info["handled"] is True
    assert info["user_message"] == "Không thể xử lý yêu cầu."
    assert info["internal_log_location"] == "evidence/logs/errors.log"
    serialized = json.dumps(info)
    assert "private" not in serialized
    assert "sqlite3 failed" not in serialized
