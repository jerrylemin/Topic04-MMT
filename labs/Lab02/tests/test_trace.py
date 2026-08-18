from app import create_app


NATIVE_OK = {
    "binary": "vulnerable_asan",
    "build_profile": "Vulnerable AddressSanitizer",
    "pid": 123,
    "timeout": False,
    "exit_code": 0,
    "signal": None,
    "stdout": "Processed name",
    "stderr": "",
    "asan": {"detected": False},
    "crash_detected": False,
    "duration_ms": 1.0,
    "status": "completed",
}


def test_trace_round_trip_and_clear(monkeypatch, tmp_path):
    monkeypatch.setattr("app.run_native", lambda *_args, **_kwargs: NATIVE_OK)
    client = create_app({"TESTING": True, "TRACE_DIR": tmp_path}).test_client()
    local = {
        "base_url": "http://127.0.0.1:5002",
        "headers": {"Accept": "application/json", "Origin": "http://127.0.0.1:5002"},
    }

    response = client.post("/submit", data={"name": "A" * 32}, **local)
    trace = response.get_json()["trace"]
    trace_id = trace["trace_id"]

    assert response.status_code == 200
    assert response.headers["X-Trace-ID"] == trace_id
    assert trace["input_length_bytes"] == 32
    assert trace["overflow_bytes"] == 1
    assert len(trace["steps"]) == 12
    assert all(
        {"step_number", "timestamp", "layer", "title", "description", "technique",
         "input_data", "output_data", "code_reference", "security_meaning", "status"}
        <= step.keys()
        for step in trace["steps"]
    )
    assert client.get(f"/api/trace/{trace_id}", **local).get_json()["trace_id"] == trace_id
    assert client.post("/api/trace/clear", **local).get_json() == {"cleared": 1}
    assert client.get(f"/api/trace/{trace_id}", **local).status_code == 404


def test_secure_rejection_is_not_reported_as_an_overflow(monkeypatch, tmp_path):
    rejected = {**NATIVE_OK, "binary": "secure_snprintf", "exit_code": 67}
    monkeypatch.setattr("app.run_native", lambda *_args, **_kwargs: rejected)
    client = create_app({"TESTING": True, "TRACE_DIR": tmp_path}).test_client()

    response = client.post(
        "/secure/snprintf/submit",
        data={"name": "A" * 64},
        base_url="http://127.0.0.1:5002",
        headers={"Accept": "application/json"},
    )
    result = response.get_json()["trace"]["final_result"]

    assert result["rejected"] is True
    assert result["overflow"] is False
    assert result["would_overflow_without_validation"] is True
