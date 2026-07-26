import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv("LAB03_SECRET_KEY", "lab03-local-demo-key-not-for-production")
    DATABASE = os.getenv("DATABASE_PATH", os.getenv("DATABASE", str(Path(__file__).with_name("lab03.db"))))
    BIND_HOST = os.getenv("LAB03_BIND_HOST", "127.0.0.1")
    MAX_CONTENT_LENGTH = 64 * 1024
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
