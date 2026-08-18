"""Run real local HTTP flows; browser-only SameSite/SOP remains manual evidence."""

import json
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config import Config  # noqa: E402
from database import init_db, query_one  # noqa: E402
from seed import reset_database  # noqa: E402
from send_legitimate_request import VICTIM_URL, extract_csrf_token, login, require_local_victim  # noqa: E402
from victim_app import create_app  # noqa: E402


def _reset() -> None:
    app = create_app({"DATABASE": Config.DATABASE})
    with app.app_context():
        init_db()
        reset_database()


def _email() -> str:
    app = create_app({"DATABASE": Config.DATABASE})
    with app.app_context():
        return query_one("SELECT email FROM users WHERE username = ?", ("victim",))["email"]


def _observation(response: requests.Response) -> dict:
    request = response.request
    return {
        "request": {
            "method": request.method,
            "url": request.url,
            "origin": request.headers.get("Origin"),
            "referer": request.headers.get("Referer"),
            "cookie_present": bool(request.headers.get("Cookie")),
            "csrf_token_present": "csrf_token=" in (request.body or ""),
        },
        "response": {
            "status": response.status_code,
            "location": response.headers.get("Location"),
            "content_type": response.headers.get("Content-Type"),
        },
    }


def run_demo_flows(base_url: str = VICTIM_URL) -> dict:
    base_url = require_local_victim(base_url)
    _reset()
    results = {
        "scope": "local requests.Session server-logic observations",
        "browser_claims": "SameSite cookie decisions and SOP response readability require manual DevTools evidence.",
        "initial_email": _email(),
        "flows": {},
    }
    with requests.Session() as session:
        results["flows"]["login"] = _observation(login(session, base_url))

        vulnerable = session.post(
            f"{base_url}/vulnerable/change-email",
            data={"email": "attacker_set@lab.local"},
            headers={
                "Origin": "http://127.0.0.1:9004",
                "Referer": "http://127.0.0.1:9004/attack/vulnerable-email",
            },
            timeout=5,
        )
        results["flows"]["vulnerable_server_logic"] = _observation(vulnerable)
        results["email_after_vulnerable"] = _email()

        missing = session.post(
            f"{base_url}/secure/change-email",
            data={"email": "missing_token@lab.local"},
            headers={"Origin": "http://127.0.0.1:9004"},
            timeout=5,
        )
        results["flows"]["secure_attacker_origin_missing_token"] = _observation(missing)

        bad = session.post(
            f"{base_url}/secure/change-email",
            data={"email": "bad_token@lab.local", "csrf_token": "invalid-demo-token"},
            headers={"Origin": base_url, "Referer": f"{base_url}/secure/change-email"},
            timeout=5,
        )
        results["flows"]["secure_bad_token"] = _observation(bad)

        form = session.get(f"{base_url}/secure/change-email", timeout=5)
        token = extract_csrf_token(form.text)
        secure = session.post(
            f"{base_url}/secure/change-email",
            data={"email": "legitimate_secure@lab.local", "csrf_token": token},
            headers={"Origin": base_url, "Referer": f"{base_url}/secure/change-email"},
            timeout=5,
        )
        results["flows"]["secure_legitimate"] = _observation(secure)
        results["email_after_secure"] = _email()
    return results


def main() -> int:
    results = run_demo_flows()
    print(json.dumps(results, ensure_ascii=False, indent=2))
    statuses = [item["response"]["status"] for item in results["flows"].values()]
    return 0 if statuses == [303, 200, 403, 403, 200] else 1


if __name__ == "__main__":
    raise SystemExit(main())
