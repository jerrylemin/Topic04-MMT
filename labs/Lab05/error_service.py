import re
import sqlite3
import uuid


PATH_PATTERN = re.compile(r"(?:[A-Za-z]:[\\/]|/)[^\s]+")
HEX_DIGEST_PATTERN = re.compile(r"\b[a-fA-F0-9]{64}\b")


def categorize_database_error(error: Exception | None) -> str | None:
    if error is None:
        return None
    message = str(error).lower()
    if isinstance(error, sqlite3.OperationalError) and any(
        marker in message for marker in ("syntax", "token", "incomplete input", "near")
    ):
        return "sql_syntax_error"
    if isinstance(error, sqlite3.DatabaseError):
        return "database_error"
    return "internal_error"


def error_inspector(error: Exception, *, secure: bool) -> dict:
    error_id = uuid.uuid4().hex[:12]
    category = categorize_database_error(error)
    if secure:
        return {
            "error_id": error_id,
            "category": category,
            "handled": True,
            "user_message": "Không thể xử lý yêu cầu.",
            "internal_log_location": "evidence/logs/errors.log",
        }
    shortened = HEX_DIGEST_PATTERN.sub("[DIGEST REDACTED]", PATH_PATTERN.sub("[PATH REDACTED]", str(error)))[:160]
    return {
        "error_id": error_id,
        "category": category,
        "exception_class": type(error).__name__,
        "shortened_message": shortened,
        "handled": True,
        "user_message": "Lỗi truy vấn đã được xử lý trong Lab05 local.",
        "database_modified": False,
    }
