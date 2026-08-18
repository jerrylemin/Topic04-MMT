from app import create_app


def test_submit_enforces_utf8_name_and_request_limits(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "app.run_native",
        lambda mode, name, **_: {
            "binary": mode,
            "build_profile": mode,
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
        },
    )
    app = create_app({"TESTING": True, "TRACE_DIR": tmp_path})
    client = app.test_client()
    local = {
        "base_url": "http://127.0.0.1:5002",
        "headers": {"Accept": "application/json"},
    }

    assert client.post("/submit", data={"name": "é" * 128}, **local).status_code == 200
    assert client.post("/submit", data={"name": "é" * 129}, **local).status_code == 400
    assert client.post(
        "/submit",
        data=b"x" * 4097,
        content_type="application/x-www-form-urlencoded",
        **local,
    ).status_code == 413
