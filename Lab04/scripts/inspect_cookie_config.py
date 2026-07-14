"""Show configured cookie policy and optionally observe a local Set-Cookie header."""

import argparse
import json
import re
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from send_legitimate_request import VICTIM_URL, require_local_victim


def mask_set_cookie(value: str) -> str:
    return re.sub(r"^(lab04_session=)[^;]+", r"\1<masked>", value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--observe", action="store_true", help="log in locally and inspect the actual response header")
    args = parser.parse_args()
    from config import Config

    print(json.dumps({
        "source": "configured expectation",
        "name": Config.SESSION_COOKIE_NAME,
        "httponly": Config.SESSION_COOKIE_HTTPONLY,
        "samesite": Config.SESSION_COOKIE_SAMESITE,
        "secure": Config.SESSION_COOKIE_SECURE,
        "path": Config.SESSION_COOKIE_PATH,
    }, indent=2))
    if args.observe:
        base_url = require_local_victim(VICTIM_URL)
        response = requests.post(
            f"{base_url}/login",
            data={"username": "victim", "password": "Victim123!"},
            timeout=5,
            allow_redirects=False,
        )
        print("observed Set-Cookie:", mask_set_cookie(response.headers.get("Set-Cookie", "<missing>")))
    print("SameSite inclusion is a browser observation; this script does not simulate it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
