"""Print the expected local origin/site matrix; no browser result is fabricated."""

import json
from urllib.parse import urlsplit


VICTIM = "http://127.0.0.1:5004"
ATTACKERS = ("http://127.0.0.1:9004", "http://localhost:9004")


def origin(url: str) -> tuple[str, str, int]:
    parsed = urlsplit(url)
    return parsed.scheme, parsed.hostname, parsed.port


def site(url: str) -> tuple[str, str]:
    parsed = urlsplit(url)
    return parsed.scheme, parsed.hostname


def matrix() -> list[dict]:
    return [{
        "victim": VICTIM,
        "attacker": attacker,
        "same_origin": origin(attacker) == origin(VICTIM),
        "same_site": site(attacker) == site(VICTIM),
        "classification": "expected from URL semantics; verify cookie behavior in DevTools",
    } for attacker in ATTACKERS]


def main() -> int:
    print(json.dumps(matrix(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
