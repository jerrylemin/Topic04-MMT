from app import create_app


def test_health_is_available_only_for_local_hosts():
    client = create_app({"TESTING": True}).test_client()

    assert client.get("/health", base_url="http://127.0.0.1:5002").get_json() == {
        "status": "ok",
        "service": "lab02",
    }
    assert client.get("/health", headers={"Host": "example.com"}).status_code == 400


def test_all_documented_pages_render():
    client = create_app({"TESTING": True}).test_client()
    local = {"base_url": "http://127.0.0.1:5002"}

    for path in (
        "/",
        "/vulnerable",
        "/secure/length",
        "/secure/snprintf",
        "/hardening",
        "/gdb-guide",
        "/comparison",
    ):
        assert client.get(path, **local).status_code == 200, path


def test_documented_submit_routes_render_their_trace(monkeypatch, tmp_path):
    def native_result(mode, *_args, **_kwargs):
        return {
            "binary": mode,
            "build_profile": mode,
            "pid": 42,
            "timeout": False,
            "exit_code": 0,
            "signal": None,
            "stdout": "Processed name: Le Minh",
            "stderr": "",
            "asan": {"detected": False},
            "crash_detected": False,
            "duration_ms": 1.0,
            "status": "completed",
        }

    monkeypatch.setattr("app.run_native", native_result)
    client = create_app({"TESTING": True, "TRACE_DIR": tmp_path}).test_client()
    local = {
        "base_url": "http://127.0.0.1:5002",
        "headers": {"Origin": "http://127.0.0.1:5002"},
    }

    for path, mode in (
        ("/submit", "vulnerable_asan"),
        ("/secure/length/submit", "secure_length"),
        ("/secure/snprintf/submit", "secure_snprintf"),
        ("/submit", "secure_hardened"),
    ):
        response = client.post(path, data={"name": "Le Minh", "mode": mode}, **local)
        assert response.status_code == 200, (path, mode)
        assert response.headers["X-Lab-Mode"] == mode
        assert response.headers["X-Trace-ID"]
