"""Smoke-test only the fixed Lab05 loopback endpoint."""

from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "http://127.0.0.1:5005"
LOG = ROOT / "evidence" / "logs" / "runtime_smoke_test.txt"
AUTH_LOGIC_INPUT = "admin_lab' -- "
SEARCH_EXPANDED_INPUT = "%' OR 1=1 -- "


def main() -> int:
    rows: list[tuple[str, bool, str]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        rows.append((name, bool(condition), detail))

    with requests.Session() as session:
        reset = session.post(f"{BASE_URL}/reset-lab", timeout=10)
        check("Reset fixed local database", reset.status_code == 200, f"HTTP {reset.status_code}")

        health = session.get(f"{BASE_URL}/health", timeout=5)
        check("Healthcheck", health.status_code == 200 and health.json().get("status") == "ok", f"HTTP {health.status_code}")
        home = session.get(f"{BASE_URL}/", timeout=5)
        check("Home", home.status_code == 200, f"HTTP {home.status_code}")

        vulnerable_login = session.post(
            f"{BASE_URL}/vulnerable/login",
            data={"username": "admin_lab", "password": "AdminLab123!"},
            timeout=10,
        )
        check("Normal vulnerable login", vulnerable_login.headers.get("X-Lab-Decision") == "authenticated",
              vulnerable_login.headers.get("X-Lab-Decision", "missing decision"))
        session.post(f"{BASE_URL}/logout", timeout=5)

        bypass = session.post(
            f"{BASE_URL}/vulnerable/login",
            data={"username": AUTH_LOGIC_INPUT, "password": "wrong-local-demo"},
            timeout=10,
        )
        check("Fixed local authentication logic demo", bypass.headers.get("X-Lab-Decision") == "local_demo_bypass",
              bypass.headers.get("X-Lab-Decision", "missing decision"))
        session.post(f"{BASE_URL}/logout", timeout=5)

        secure_reject = session.post(
            f"{BASE_URL}/secure/login",
            data={"username": AUTH_LOGIC_INPUT, "password": "wrong-local-demo"},
            timeout=10,
        )
        check("Secure login rejects same input", secure_reject.headers.get("X-Lab-Decision") == "rejected",
              secure_reject.headers.get("X-Lab-Decision", "missing decision"))

        secure_login = session.post(
            f"{BASE_URL}/secure/login",
            data={"username": "admin_lab", "password": "AdminLab123!"},
            timeout=10,
        )
        check("Normal secure login", secure_login.headers.get("X-Lab-Decision") == "authenticated",
              secure_login.headers.get("X-Lab-Decision", "missing decision"))

        normal_search = session.get(f"{BASE_URL}/vulnerable/search", params={"keyword": "USB"}, timeout=5)
        normal_count = int(normal_search.headers.get("X-Lab-Result-Count", "0"))
        check("Normal vulnerable search", normal_search.status_code == 200 and normal_count >= 1,
              f"rows={normal_count}")

        expanded = session.get(f"{BASE_URL}/vulnerable/search", params={"keyword": SEARCH_EXPANDED_INPUT}, timeout=5)
        expanded_count = int(expanded.headers.get("X-Lab-Result-Count", "0"))
        check("Expanded vulnerable product search", expanded_count > normal_count, f"rows={expanded_count}")

        secure_search = session.get(f"{BASE_URL}/secure/search", params={"keyword": SEARCH_EXPANDED_INPUT}, timeout=5)
        check("Secure search preserves structure",
              secure_search.headers.get("X-Lab-Prepared") == "true"
              and secure_search.headers.get("X-Lab-Result-Count") == "0",
              f"prepared={secure_search.headers.get('X-Lab-Prepared')}, rows={secure_search.headers.get('X-Lab-Result-Count')}")

        detail = session.get(f"{BASE_URL}/secure/user", params={"id": 1}, timeout=5)
        check("Secure user detail", detail.status_code == 200 and detail.headers.get("X-Lab-Prepared") == "true",
              f"HTTP {detail.status_code}")
        check("Security headers",
              home.headers.get("X-Content-Type-Options") == "nosniff"
              and home.headers.get("X-Frame-Options") == "DENY"
              and "unsafe-eval" not in home.headers.get("Content-Security-Policy", ""),
              "CSP/nosniff/frame policy")

    passed = sum(item[1] for item in rows)
    lines = ["LAB05 RUNTIME SMOKE TEST", f"Target: {BASE_URL} only", ""]
    lines.extend(f"{'PASS' if ok else 'FAIL'} | {name} | {detail}" for name, ok, detail in rows)
    lines.extend(("", f"Result: {passed}/{len(rows)} checks passed"))
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[-1])
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
