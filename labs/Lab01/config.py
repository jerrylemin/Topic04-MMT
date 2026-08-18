import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "local-lab-only-not-a-real-secret")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    DATABASE = os.getenv("DATABASE", "lab01.db")
