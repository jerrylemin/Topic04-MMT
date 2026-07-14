"""Smoke-test the fixed loopback services; no browser behavior is claimed."""

import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from send_legitimate_request import extract_csrf_token  # noqa: E402


VICTIM = "http://127.0.0.1:5004"
DEMO = "http://127.0.0.1:9004"
ORIGIN = {"Origin": VICTIM, "Referer": f"{VICTIM}/dashboard"}
LOG = ROOT / "evidence/logs/runtime_smoke_test.txt"


def main() -> int:
    rows = []

    def check(name, response, expected):
        passed = response.status_code in expected
        rows.append((name, response.status_code, sorted(expected), passed))
        return response

    with requests.Session() as session:
        check("Healthcheck Victim", session.get(f"{VICTIM}/health", timeout=5), {200})
        check("Healthcheck Demo Page", session.get(f"{DEMO}/health", timeout=5), {200})
        check("Login victim", session.post(f"{VICTIM}/login", data={"username": "victim", "password": "Victim123!"}, allow_redirects=False, timeout=5), {303})
        check("Vulnerable email change", session.post(f"{VICTIM}/vulnerable/change-email", data={"email": "runtime_demo@lab.local"}, headers={"Origin": DEMO}, timeout=5), {200})

        dashboard = session.get(f"{VICTIM}/dashboard", timeout=5)
        check("Reset valid token", session.post(f"{VICTIM}/reset-lab", data={"csrf_token": extract_csrf_token(dashboard.text)}, headers=ORIGIN, allow_redirects=False, timeout=5), {303})
        check("Login after reset", session.post(f"{VICTIM}/login", data={"username": "victim", "password": "Victim123!"}, allow_redirects=False, timeout=5), {303})

        check("Secure email missing token", session.post(f"{VICTIM}/secure/change-email", data={"email": "missing@lab.local"}, headers=ORIGIN, timeout=5), {403})
        check("Secure email invalid token", session.post(f"{VICTIM}/secure/change-email", data={"email": "invalid@lab.local", "csrf_token": "x" * 43}, headers=ORIGIN, timeout=5), {403})
        form = session.get(f"{VICTIM}/secure/change-email", timeout=5)
        token = extract_csrf_token(form.text)
        check("Secure email Origin denied", session.post(f"{VICTIM}/secure/change-email", data={"email": "origin@lab.local", "csrf_token": token}, headers={"Origin": DEMO}, timeout=5), {403})
        check("Secure email success", session.post(f"{VICTIM}/secure/change-email", data={"email": "runtime_secure@lab.local", "csrf_token": token}, headers=ORIGIN, timeout=5), {200})
        check("Logout missing token", session.post(f"{VICTIM}/logout", headers=ORIGIN, timeout=5), {403})
        form = session.get(f"{VICTIM}/dashboard", timeout=5)
        check("Logout success", session.post(f"{VICTIM}/logout", data={"csrf_token": extract_csrf_token(form.text)}, headers=ORIGIN, allow_redirects=False, timeout=5), {303})

    lines = ["LAB04 RUNTIME SMOKE TEST", "Scope: fixed localhost endpoints; no SameSite/SOP browser claim.", ""]
    lines.extend(f"{'PASS' if passed else 'FAIL'} | {name} | HTTP {status} | expected {expected}" for name, status, expected, passed in rows)
    lines.append("")
    lines.append(f"Result: {sum(row[3] for row in rows)}/{len(rows)} checks passed")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[-1])
    return 0 if all(row[3] for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
