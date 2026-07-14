import subprocess

import native_runner
from app import create_app
from native_runner import run_native
from security_utils import parse_asan, redact_text


def test_native_runner_uses_fixed_argv_cwd_timeout_and_environment(monkeypatch, tmp_path):
    build = tmp_path / "build"
    build.mkdir()
    (build / "processor").write_text("binary", encoding="utf-8")
    captured = {}

    def fake_run(argv, **kwargs):
        captured.update(argv=argv, **kwargs)
        return subprocess.CompletedProcess(argv, 0, "PID: 42\nProcessed name: A\n", "")

    monkeypatch.setattr(native_runner.subprocess, "run", fake_run)
    result = run_native(
        "safe",
        "A; echo ignored",
        modes={"safe": {"binary": "processor", "profile": "safe", "flags": "-O2"}},
        root=tmp_path,
        timeout=1.25,
    )

    assert captured["argv"] == [str((build / "processor").resolve()), "A; echo ignored"]
    assert captured["shell"] is False
    assert captured["cwd"] == str(tmp_path.resolve())
    assert captured["timeout"] == 1.25
    assert captured["env"] == native_runner.restricted_environment()
    assert "HOME" not in captured["env"] and result["pid"] == 42


def test_external_origin_is_rejected_before_native_execution(monkeypatch, tmp_path):
    called = False

    def should_not_run(*_args, **_kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr("app.run_native", should_not_run)
    client = create_app({"TESTING": True, "TRACE_DIR": tmp_path}).test_client()
    response = client.post(
        "/submit",
        data={"name": "Le Minh"},
        base_url="http://127.0.0.1:5002",
        headers={"Origin": "https://example.com", "Accept": "application/json"},
    )

    assert response.status_code == 403
    assert called is False


def test_mode_allowlist_and_debug_guard_block_uncontrolled_runs(monkeypatch, tmp_path):
    called = False

    def should_not_run(*_args, **_kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr("app.run_native", should_not_run)
    client = create_app({"TESTING": True, "TRACE_DIR": tmp_path}).test_client()
    local = {
        "base_url": "http://127.0.0.1:5002",
        "headers": {"Accept": "application/json"},
    }

    assert client.post("/submit", data={"name": "A", "mode": "../../bin/sh"}, **local).status_code == 400
    assert client.post(
        "/submit", data={"name": "A" * 64, "mode": "vulnerable_debug"}, **local
    ).status_code == 400
    assert called is False


def test_asan_parser_and_response_redaction_hide_home_paths(tmp_path):
    log = (
        "==1==ERROR: AddressSanitizer: stack-buffer-overflow\n"
        "WRITE of size 65 at 0x00\n"
        f"    #0 0x00 in process_name {tmp_path}/native/vulnerable_processor.c:8:5\n"
        "  [32, 64) 'name'\n"
        "/home/student/private/token.txt\n"
    )

    parsed = parse_asan(log, tmp_path, 64)
    cleaned = redact_text(log, tmp_path)

    assert parsed["detected"] is True
    assert parsed["error_type"] == "stack-buffer-overflow"
    assert parsed["write_size"] == 65
    assert parsed["buffer_name"] == "name"
    assert str(tmp_path) not in cleaned
    assert "/home/student" not in cleaned
