from dataclasses import dataclass
from urllib.parse import urlsplit


ALLOWED_ORIGINS = frozenset({"http://127.0.0.1:5004", "http://localhost:5004"})


@dataclass(frozen=True)
class OriginDecision:
    allowed: bool
    source: str
    reason: str
    origin: str | None
    referer: str | None
    parsed: dict | None
    expected_origins: tuple[str, ...] = tuple(sorted(ALLOWED_ORIGINS))

    def to_dict(self) -> dict:
        parsed_origin = parse_origin(self.origin)
        parsed_referer = parse_origin(self.referer, allow_path=True)
        return {
            "origin_raw": self.origin,
            "referer_raw": self.referer,
            "parsed_origin": parsed_origin,
            "parsed_referer": parsed_referer,
            "expected_origins": self.expected_origins,
            "origin_match": bool(parsed_origin and parsed_origin["origin"] in self.expected_origins),
            "referer_match": bool(parsed_referer and parsed_referer["origin"] in self.expected_origins),
            "decision": "allowed" if self.allowed else "denied",
            "reason": self.reason,
        }


def parse_origin(value: str | None, *, allow_path: bool = False) -> dict | None:
    if not value or any(char.isspace() for char in value):
        return None
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return None
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        return None
    if not allow_path and (parsed.path or parsed.query or parsed.fragment):
        return None
    if port is None:
        port = 443 if parsed.scheme == "https" else 80
    hostname = parsed.hostname.lower()
    host = f"[{hostname}]" if ":" in hostname else hostname
    return {"scheme": parsed.scheme, "hostname": hostname, "port": port, "origin": f"{parsed.scheme}://{host}:{port}"}


def validate_origin_or_referer(origin: str | None, referer: str | None = None,
                               allowed_origins=ALLOWED_ORIGINS) -> OriginDecision:
    if hasattr(origin, "headers"):
        referer = origin.headers.get("Referer")
        origin = origin.headers.get("Origin")
    if origin:
        parsed = parse_origin(origin)
        allowed = bool(parsed and parsed["origin"] in allowed_origins)
        return OriginDecision(allowed, "origin", "origin_allowed" if allowed else "origin_denied",
                              origin, referer, parsed)
    if referer:
        parsed = parse_origin(referer, allow_path=True)
        allowed = bool(parsed and parsed["origin"] in allowed_origins)
        return OriginDecision(allowed, "referer", "referer_allowed" if allowed else "referer_denied",
                              origin, referer, parsed)
    return OriginDecision(False, "none", "origin_and_referer_missing", origin, referer, None)


def origin_matches(value: str | None, allowed_origins=ALLOWED_ORIGINS) -> bool:
    parsed = parse_origin(value)
    return bool(parsed and parsed["origin"] in allowed_origins)
