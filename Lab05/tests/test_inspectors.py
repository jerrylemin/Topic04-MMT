import pytest


@pytest.fixture()
def secure_search_trace(shared_client):
    response = shared_client.get("/secure/search", query_string={"keyword": "USB"})
    return shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()


@pytest.mark.parametrize("panel", [
    "request_inspector", "input_inspector", "query_inspector", "execution_inspector",
    "decision_inspector", "result_set_inspector", "database_inspector", "audit_inspector",
    "final_verdict",
])
def test_trace_exposes_required_inspector_panel(secure_search_trace, panel):
    assert isinstance(secure_search_trace[panel], dict)
    assert secure_search_trace[panel]


def test_request_inspector_comes_from_real_request(secure_search_trace):
    inspector = secure_search_trace["request_inspector"]
    assert inspector["method"] == "GET"
    assert inspector["path"] == "/secure/search"
    assert inspector["query_string"] == "keyword=USB"
    assert inspector["route_handler"] == "secure_search_route"


def test_input_inspector_marks_untrusted_source(secure_search_trace):
    inspector = secure_search_trace["input_inspector"]
    assert inspector["raw_input"] == "USB"
    assert inspector["source"] == "request.args"
    assert inspector["trust_level"] == "untrusted"
    assert inspector["validation_result"] == "accepted"


def test_execution_inspector_uses_safe_database_label(secure_search_trace):
    inspector = secure_search_trace["execution_inspector"]
    assert inspector["database_label"] == "Lab05 local SQLite"
    assert inspector["operation"] == "SELECT"
    assert inspector["read_only"] if "read_only" in inspector else inspector["transaction_status"] == "read_only"
    assert ":\\" not in jsonish(inspector)


def jsonish(value):
    import json
    return json.dumps(value, ensure_ascii=False)


def test_final_verdict_reflects_runtime_controls(secure_search_trace):
    verdict = secure_search_trace["final_verdict"]
    assert verdict["prepared_statement_used"] is True
    assert verdict["sql_structure_changed"] is False
    assert verdict["database_modified"] is False
    assert verdict["sensitive_data_exposed"] is False
    assert verdict["audit_event"] == "secure_search_completed"


def test_audit_inspector_is_linked_to_same_trace(secure_search_trace):
    audit = secure_search_trace["audit_inspector"]
    assert audit["action"] == "secure_search_completed"
    assert audit["trace_id"] == secure_search_trace["trace_id"]
    assert audit["decision"] == "expected_results"


def test_code_comparison_contains_real_source_ranges(secure_search_trace):
    comparison = secure_search_trace["code_comparison"]
    assert comparison["vulnerable_file"] == "vulnerable_queries.py"
    assert comparison["secure_file"] == "secure_queries.py"
    assert "def vulnerable_search" in comparison["vulnerable_code"]
    assert "def secure_search" in comparison["secure_code"]
