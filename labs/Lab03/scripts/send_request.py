from __future__ import annotations

import argparse
import json

import requests

BASE_URL = "http://127.0.0.1:5003"
SCENARIOS = {
    "login-user-a": ("POST", "/login", {"username": "user_a", "password": "UserA123!"}),
    "checkout-normal-vulnerable": ("POST", "/vulnerable/checkout", {"product_id": 5, "quantity": 1, "price": 100000}),
    "checkout-price-1-vulnerable": ("POST", "/vulnerable/checkout", {"product_id": 5, "quantity": 1, "price": 1}),
    "checkout-price-1-secure": ("POST", "/secure/checkout", {"product_id": 5, "quantity": 1, "price": 1}),
    "invoice-1001-vulnerable": ("GET", "/vulnerable/invoice", {"id": 1001}),
    "invoice-1002-vulnerable": ("GET", "/vulnerable/invoice", {"id": 1002}),
    "invoice-1002-secure": ("GET", "/secure/invoice", {"id": 1002}),
    "profile-normal-vulnerable": ("POST", "/vulnerable/profile/update", {"user_id": 12, "email": "usera@lab.local", "role": "user"}),
    "profile-admin-vulnerable": ("POST", "/vulnerable/profile/update", {"user_id": 12, "email": "usera@lab.local", "role": "admin"}),
    "profile-admin-secure": ("POST", "/secure/profile/update", {"user_id": 12, "email": "usera@lab.local", "role": "admin"}),
}


def trace_id(response: requests.Response) -> str:
    marker = 'data-trace-id="'
    return response.text.split(marker, 1)[1].split('"', 1)[0] if marker in response.text else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Gửi một scenario cố định tới Lab03 localhost.")
    parser.add_argument("--scenario", required=True, choices=SCENARIOS)
    args = parser.parse_args()
    session = requests.Session()
    if args.scenario != "login-user-a":
        login = session.post(f"{BASE_URL}/login", data={"username": "user_a", "password": "UserA123!"}, timeout=5)
        login.raise_for_status()
    method, route, parameters = SCENARIOS[args.scenario]
    response = session.request(method, f"{BASE_URL}{route}", params=parameters if method == "GET" else None,
                               data=parameters if method == "POST" else None, timeout=5, allow_redirects=True)
    tid = trace_id(response)
    trace = session.get(f"{BASE_URL}/api/trace/{tid}", timeout=5).json() if tid else {}
    public_parameters = {key: "***" if key == "password" else value for key, value in parameters.items()}
    print(json.dumps({"http_status": response.status_code, "current_user": trace.get("current_user", {}).get("username", "user_a"),
                      "submitted_parameters": public_parameters, "trace_id": tid,
                      "decision": trace.get("final_verdict", {}).get("success"),
                      "final_result": trace.get("final_verdict", {}) or response.url}, ensure_ascii=True, indent=2))
    return 0 if response.status_code < 500 else 1


if __name__ == "__main__":
    raise SystemExit(main())
