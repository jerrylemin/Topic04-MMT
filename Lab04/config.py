import os
import secrets
from pathlib import Path


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    return default if value is None else value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    SECRET_KEY = os.getenv("VICTIM_SECRET_KEY") or os.getenv("LAB04_SECRET_KEY") or secrets.token_hex(32)
    DATABASE = os.getenv("DATABASE") or os.getenv("LAB04_DATABASE") or str(Path(__file__).with_name("lab04.sqlite3"))
    MAX_CONTENT_LENGTH = 64 * 1024
    SESSION_COOKIE_NAME = "lab04_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE") or os.getenv("LAB04_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = (_env_bool("SESSION_COOKIE_SECURE") if os.getenv("SESSION_COOKIE_SECURE") is not None
                             else _env_bool("LAB04_COOKIE_SECURE"))
    SESSION_COOKIE_PATH = "/"
    PERMANENT_SESSION_LIFETIME = 3600
