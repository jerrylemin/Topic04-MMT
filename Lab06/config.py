from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parent
_PROCESS_SECRET = "lab06-local-demo-key-not-for-production"
_PROCESS_SIGNING_KEY = "lab06-local-signing-key-not-for-production"
_PROCESS_FERNET_KEY = "MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA="


class Config:
    HOST = "127.0.0.1"
    PORT = 5006
    DEBUG = False
    TESTING = False
    DATABASE = os.environ.get("LAB06_DATABASE", str(ROOT / "instance" / "lab06.sqlite3"))
    SECRET_KEY = os.environ.get("LAB06_SECRET_KEY", _PROCESS_SECRET)
    SIGNING_KEY = os.environ.get("LAB06_SIGNING_KEY", _PROCESS_SIGNING_KEY)
    FERNET_KEY = os.environ.get("LAB06_FERNET_KEY", _PROCESS_FERNET_KEY)
    COOKIE_SECURE = os.environ.get("LAB06_COOKIE_SECURE", "false").lower() == "true"
    SESSION_TTL_SECONDS = int(os.environ.get("LAB06_SESSION_TTL_SECONDS", "1800"))
    MAX_CONTENT_LENGTH = int(os.environ.get("LAB06_MAX_CONTENT_LENGTH", "65536"))
    EVIDENCE_DIR = os.environ.get("LAB06_EVIDENCE_DIR", str(ROOT / "evidence"))
    JSON_SORT_KEYS = True


BaseConfig = Config


@dataclass(frozen=True, slots=True)
class LabConfig:
    host: str
    port: int
    debug: bool
    database_path: Path
    evidence_dir: Path
    signing_secret: str
    fernet_key: bytes
    cookie_secure: bool
    session_ttl_seconds: int
    max_content_length: int


def load_config(environ: Mapping[str, str] | None = None) -> LabConfig:
    env = os.environ if environ is None else environ
    config = LabConfig(
        host="127.0.0.1",
        port=5006,
        debug=False,
        database_path=Path(env.get("LAB06_DATABASE", Config.DATABASE)),
        evidence_dir=Path(env.get("LAB06_EVIDENCE_DIR", Config.EVIDENCE_DIR)),
        signing_secret=env.get("LAB06_SIGNING_KEY", _PROCESS_SIGNING_KEY),
        fernet_key=env.get("LAB06_FERNET_KEY", _PROCESS_FERNET_KEY).encode("ascii"),
        cookie_secure=env.get("LAB06_COOKIE_SECURE", "false").lower() == "true",
        session_ttl_seconds=int(env.get("LAB06_SESSION_TTL_SECONDS", "1800")),
        max_content_length=int(env.get("LAB06_MAX_CONTENT_LENGTH", "65536")),
    )
    validate_config(config)
    return config


def validate_config(config: LabConfig) -> None:
    if config.host != "127.0.0.1" or config.port != 5006 or config.debug:
        raise ValueError("Lab06 must run at 127.0.0.1:5006 with debug disabled")
    if config.session_ttl_seconds < 60:
        raise ValueError("Session lifetime must be at least 60 seconds")
    if config.max_content_length <= 0:
        raise ValueError("MAX_CONTENT_LENGTH must be positive")


def _config_value(config: LabConfig | Mapping[str, Any] | Any, name: str) -> Any:
    if isinstance(config, LabConfig):
        return getattr(config, name.lower())
    if isinstance(config, Mapping):
        return config[name]
    return getattr(config, name)


# LAB06-CODE:cookie_flags:START
def cookie_options(
    config: LabConfig | Mapping[str, Any] | Any,
    *,
    httponly: bool,
    max_age: int | None = None,
) -> dict[str, object]:
    options: dict[str, object] = {
        "path": "/",
        "secure": bool(_config_value(config, "COOKIE_SECURE")),
        "httponly": httponly,
        "samesite": "Lax",
    }
    if max_age is not None:
        options["max_age"] = max_age
    return options
# LAB06-CODE:cookie_flags:END
