"""Smoke-test only the fixed live Lab06 endpoint at 127.0.0.1:5006."""

from __future__ import annotations

import sys
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from base64_cookie_service import BASE64_COOKIE, encode_profile, modified_demo_profile  # noqa: E402
from server_session_service import SESSION_COOKIE  # noqa: E402
from signed_cookie_service import SIGNED_COOKIE  # noqa: E402


BASE_URL = "http://127.0.0.1:5006"
LOG = ROOT / "evidence" / "logs" / "runtime_smoke.txt"
LEGACY_LOG = ROOT / "evidence" / "logs" / "runtime_smoke_test.txt"


def _mutate_one_character(value: str) -> str:
    index = max(1, len(value) // 2)
    replacement = "A" if value[index] != "A" else "B"
    return value[:index] + replacement + value[index + 1 :]


def main() -> int:
    rows: list[tuple[str, bool, str]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        rows.append((name, bool(condition), detail))

    try:
        control = requests.Session()
        reset = control.post(f"{BASE_URL}/reset-lab", timeout=10)
        check("Reset fixed local database", reset.status_code == 200, f"HTTP {reset.status_code}")
        health = control.get(f"{BASE_URL}/health", timeout=5)
        health_data = health.json() if health.ok else {}
        check(
            "Healthcheck",
            health.status_code == 200
            and health_data.get("status") == "ok"
            and health_data.get("host") == "127.0.0.1"
            and health_data.get("port") == 5006,
            f"HTTP {health.status_code}",
        )
        home = control.get(f"{BASE_URL}/", timeout=5)
        check("Home", home.status_code == 200, f"HTTP {home.status_code}")
        check(
            "Security headers",
            home.headers.get("X-Content-Type-Options") == "nosniff"
            and home.headers.get("X-Frame-Options") == "DENY"
            and "unsafe-eval" not in home.headers.get("Content-Security-Policy", ""),
            "CSP/nosniff/frame policy",
        )

        plain = requests.Session()
        login = plain.post(
            f"{BASE_URL}/login",
            data={"username": "student", "password": "Student123!", "mode": "plain"},
            allow_redirects=False,
            timeout=10,
        )
        check("Plain login issues cookies", 300 <= login.status_code < 400 and "lab06_role" in plain.cookies, f"HTTP {login.status_code}")
        denied = plain.get(f"{BASE_URL}/vulnerable/plain/admin", timeout=5)
        check("Plain role=user denied", denied.status_code == 403 and denied.headers.get("X-Lab-Decision") == "deny", f"HTTP {denied.status_code}")
        plain.cookies.set("lab06_role", "admin", domain="127.0.0.1", path="/")
        allowed = plain.get(f"{BASE_URL}/vulnerable/plain/admin", timeout=5)
        check("Plain role=admin local demo allowed", allowed.status_code == 200 and allowed.headers.get("X-Lab-Decision") == "allow", f"HTTP {allowed.status_code}")

        base64_client = requests.Session()
        login = base64_client.post(
            f"{BASE_URL}/login",
            data={"username": "student", "password": "Student123!", "mode": "base64"},
            allow_redirects=False,
            timeout=10,
        )
        check("Base64 login issues cookie", 300 <= login.status_code < 400 and BASE64_COOKIE in base64_client.cookies, f"HTTP {login.status_code}")
        denied = base64_client.get(f"{BASE_URL}/vulnerable/base64/admin", timeout=5)
        check("Base64 original denied", denied.status_code == 403 and denied.headers.get("X-Lab-Decision") == "deny", f"HTTP {denied.status_code}")
        base64_client.cookies.set(
            BASE64_COOKIE,
            encode_profile(modified_demo_profile()),
            domain="127.0.0.1",
            path="/",
        )
        allowed = base64_client.get(f"{BASE_URL}/vulnerable/base64/admin", timeout=5)
        check("Base64 modified local demo allowed", allowed.status_code == 200 and allowed.headers.get("X-Lab-Decision") == "allow", f"HTTP {allowed.status_code}")

        signed = requests.Session()
        login = signed.post(
            f"{BASE_URL}/login",
            data={"username": "admin_lab", "password": "AdminLab123!", "mode": "signed"},
            allow_redirects=False,
            timeout=10,
        )
        check("Signed login issues cookie", 300 <= login.status_code < 400 and SIGNED_COOKIE in signed.cookies, f"HTTP {login.status_code}")
        valid = signed.get(f"{BASE_URL}/secure/signed/admin", timeout=5)
        check("Signed valid admin allowed", valid.status_code == 200 and valid.headers.get("X-Lab-Signature-Status") == "valid", f"HTTP {valid.status_code}")
        signed_value = signed.cookies.get(SIGNED_COOKIE, domain="127.0.0.1", path="/")
        if signed_value:
            signed.cookies.set(SIGNED_COOKIE, _mutate_one_character(signed_value), domain="127.0.0.1", path="/")
        invalid = signed.get(f"{BASE_URL}/secure/signed/profile", timeout=5)
        check("Signed tamper rejected", invalid.status_code in {400, 401} and invalid.headers.get("X-Lab-Signature-Status") == "invalid", f"HTTP {invalid.status_code}")

        encrypted = control.get(f"{BASE_URL}/secure/encrypted-demo", timeout=5)
        check(
            "Encrypted read-only demo",
            encrypted.status_code == 200
            and encrypted.headers.get("X-Lab-Encryption-Status") == "valid"
            and encrypted.headers.get("X-Lab-Authorization-Used") == "false",
            f"HTTP {encrypted.status_code}",
        )

        student = requests.Session()
        login = student.post(
            f"{BASE_URL}/login",
            data={"username": "student", "password": "Student123!", "mode": "session"},
            allow_redirects=False,
            timeout=10,
        )
        check("Student server session created", 300 <= login.status_code < 400 and SESSION_COOKIE in student.cookies, f"HTTP {login.status_code}")
        denied = student.get(f"{BASE_URL}/secure/session/admin", timeout=5)
        check("Student database role denied", denied.status_code == 403 and denied.headers.get("X-Lab-Role-Source") == "database", f"HTTP {denied.status_code}")
        old_token = student.cookies.get(SESSION_COOKIE, domain="127.0.0.1", path="/")
        rotated = student.post(
            f"{BASE_URL}/login",
            data={"username": "student", "password": "Student123!", "mode": "session"},
            allow_redirects=False,
            timeout=10,
        )
        check("Session rotation", 300 <= rotated.status_code < 400 and rotated.headers.get("X-Lab-Session-Status") == "login_rotation", f"HTTP {rotated.status_code}")
        old_client = requests.Session()
        if old_token:
            old_client.cookies.set(SESSION_COOKIE, old_token, domain="127.0.0.1", path="/")
        old_rejected = old_client.get(f"{BASE_URL}/secure/session/profile", timeout=5)
        check("Old session rejected", old_rejected.status_code == 401 and old_rejected.headers.get("X-Lab-Session-Status") == "inactive_session", f"HTTP {old_rejected.status_code}")
        logout = student.post(f"{BASE_URL}/secure/session/logout", timeout=5)
        check("Logout invalidates server session", logout.status_code == 200 and logout.headers.get("X-Lab-Session-Status") == "logout_invalidated_session", f"HTTP {logout.status_code}")

        admin = requests.Session()
        login = admin.post(
            f"{BASE_URL}/login",
            data={"username": "admin_lab", "password": "AdminLab123!", "mode": "session"},
            allow_redirects=False,
            timeout=10,
        )
        admin_page = admin.get(f"{BASE_URL}/secure/session/admin", timeout=5)
        check("Admin database role allowed", 300 <= login.status_code < 400 and admin_page.status_code == 200 and admin_page.headers.get("X-Lab-Decision") == "allow", f"HTTP {admin_page.status_code}")
    except requests.RequestException as exc:
        check("Live loopback connection", False, f"{type(exc).__name__}: fixed endpoint unavailable")

    passed = sum(ok for _name, ok, _detail in rows)
    lines = ["LAB06 RUNTIME SMOKE TEST", f"Target: {BASE_URL} only", ""]
    lines.extend(f"{'PASS' if ok else 'FAIL'} | {name} | {detail}" for name, ok, detail in rows)
    lines.extend(("", f"Result: {passed}/{len(rows)} checks passed"))
    if passed == len(rows):
        lines.append("SMOKE_TEST_PASSED")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    output = "\n".join(lines) + "\n"
    LOG.write_text(output, encoding="utf-8")
    LEGACY_LOG.write_text(output, encoding="utf-8")
    print(lines[-1])
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
