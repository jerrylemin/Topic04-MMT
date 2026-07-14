import os
import secrets
from pathlib import Path


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5005
QUOTE_INPUT = "'"
AUTH_LOGIC_INPUT = "admin_lab' -- "
SEARCH_EXPANDED_INPUT = "%' OR 1=1 -- "
FIXED_TEST_INPUTS = {
    "normal_login": "admin_lab",
    "quote": QUOTE_INPUT,
    "authentication_logic": AUTH_LOGIC_INPUT,
    "normal_search": "USB",
    "expanded_search": SEARCH_EXPANDED_INPUT,
}


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    return default if value is None else value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    SECRET_KEY = os.getenv("LAB05_SECRET_KEY") or secrets.token_hex(32)
    DATABASE = os.getenv("LAB05_DATABASE") or str(Path(__file__).with_name("lab05.sqlite3"))
    SERVER_HOST = SERVER_HOST
    SERVER_PORT = SERVER_PORT
    MAX_CONTENT_LENGTH = 64 * 1024
    SESSION_COOKIE_NAME = "lab05_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _env_bool("LAB05_COOKIE_SECURE")
    PERMANENT_SESSION_LIFETIME = 3600
    TEST_INPUTS = FIXED_TEST_INPUTS
    DATABASE_LABEL = "Lab05 local SQLite"

