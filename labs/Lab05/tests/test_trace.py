import json

import pytest

from config import AUTH_LOGIC_INPUT, SEARCH_EXPANDED_INPUT


@pytest.mark.parametrize("method,path,data,expected_steps", [
    ("post", "/vulnerable/login", {"username": AUTH_LOGIC_INPUT, "password": "wrong"}, 12),
    ("post", "/secure/login", {"username": AUTH_LOGIC_INPUT, "password": "wrong"}, 10),
    ("get", "/vulnerable/search", {"keyword": SEARCH_EXPANDED_INPUT}, 9),
    ("get", "/secure/search", {"keyword": SEARCH_EXPANDED_INPUT}, 7),
])
def test_explicit_flow_timelines_have_required_step_counts(shared_client, method, path, data, expected_steps):
    kwargs = {"data": data} if method == "post" else {"query_string": data}
    response = getattr(shared_client, method)(path, **kwargs)
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    assert len(trace["steps"]) == expected_steps
    assert [step["step_number"] for step in trace["steps"]] == list(range(1, expected_steps + 1))


def test_every_trace_step_has_evidence_fields(shared_client):
    response = shared_client.get("/secure/search", query_string={"keyword": "USB"})
    steps = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()["steps"]
    required = {"step_number", "timestamp", "layer", "title", "description", "technique",
                "input_data", "output_data", "code_reference", "security_meaning", "status"}
    assert all(required <= step.keys() for step in steps)


def test_trace_request_inspector_redacts_password(shared_client):
    response = shared_client.post(
        "/secure/login", data={"username": "admin_lab", "password": "AdminLab123!"}
    )
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    request_info = trace["request_inspector"]
    assert request_info["form_values"]["password"] == "[REDACTED]"
    assert request_info["timestamp"]
    assert "AdminLab123!" not in json.dumps(trace)


def test_trace_clear_post_removes_existing_trace(shared_client, clear_events):
    response = shared_client.get("/secure/search", query_string={"keyword": "USB"})
    trace_id = response.headers["X-Lab-Trace-ID"]
    assert shared_client.get(f"/api/trace/{trace_id}").status_code == 200
    assert shared_client.post("/api/trace/clear").get_json() == {"cleared": True}
    assert shared_client.get(f"/api/trace/{trace_id}").status_code == 404


def test_trace_clear_get_does_not_remove_trace(shared_client, clear_events):
    response = shared_client.get("/secure/search", query_string={"keyword": "USB"})
    trace_id = response.headers["X-Lab-Trace-ID"]
    assert shared_client.get("/api/trace/clear").status_code == 405
    assert shared_client.get(f"/api/trace/{trace_id}").status_code == 200

