"""Send one real, local, legitimate secure email-change request."""

import os
from html.parser import HTMLParser
from urllib.parse import urlsplit

import requests


VICTIM_URL = os.getenv("LAB04_VICTIM_URL", "http://127.0.0.1:5004")


def require_local_victim(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"} or parsed.port != 5004:
        raise ValueError("Lab04 scripts only allow the local Victim Application on port 5004.")
    return url.rstrip("/")


class _TokenParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.token = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "input" and attributes.get("name") == "csrf_token":
            self.token = attributes.get("value")


def extract_csrf_token(html: str) -> str:
    parser = _TokenParser()
    parser.feed(html)
    if not parser.token:
        raise RuntimeError("Secure form did not contain csrf_token.")
    return parser.token


def login(session: requests.Session, base_url: str = VICTIM_URL) -> requests.Response:
    base_url = require_local_victim(base_url)
    response = session.post(
        f"{base_url}/login",
        data={"username": "victim", "password": "Victim123!"},
        timeout=5,
        allow_redirects=False,
    )
    if response.status_code != 303:
        raise RuntimeError(f"Login failed with HTTP {response.status_code}.")
    return response


def send_secure_email(
    session: requests.Session,
    email: str = "legitimate_secure@lab.local",
    base_url: str = VICTIM_URL,
) -> requests.Response:
    base_url = require_local_victim(base_url)
    form = session.get(f"{base_url}/secure/change-email", timeout=5)
    form.raise_for_status()
    token = extract_csrf_token(form.text)
    return session.post(
        f"{base_url}/secure/change-email",
        data={"email": email, "csrf_token": token},
        headers={"Origin": base_url, "Referer": f"{base_url}/secure/change-email"},
        timeout=5,
    )


def main() -> int:
    base_url = require_local_victim(VICTIM_URL)
    with requests.Session() as session:
        login(session, base_url)
        response = send_secure_email(session, base_url=base_url)
    print(f"Observed secure request: HTTP {response.status_code}")
    print("Browser SameSite/SOP behavior is not claimed by this requests.Session script.")
    return 0 if response.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
