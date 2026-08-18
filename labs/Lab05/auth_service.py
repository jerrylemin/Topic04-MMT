from datetime import datetime, timezone

from flask import session
from werkzeug.security import check_password_hash

from config import AUTH_LOGIC_INPUT
from secure_queries import secure_login_lookup
from vulnerable_queries import vulnerable_login


def authenticate_vulnerable(username: str, password: str) -> dict:
    rows, query = vulnerable_login(username, password)
    error = query.get("error")
    if error:
        return {"user": None, "rows": rows, "query": query, "decision": "query_error",
                "reason": "sqlite_rejected_final_sql", "password_length": len(password)}
    user = dict(rows[0]) if rows else None
    if user and username == AUTH_LOGIC_INPUT:
        decision, reason = "local_demo_bypass", "fixed_local_input_changed_where_logic"
    elif user:
        decision, reason = "authenticated", "legacy_digest_matched"
    else:
        decision, reason = "rejected", "invalid_demo_credentials"
    return {"user": user, "rows": rows, "query": query, "decision": decision,
            "reason": reason, "password_length": len(password)}


def authenticate_secure(username: str, password: str) -> dict:
    rows, query = secure_login_lookup(username)
    row = rows[0] if rows else None
    verified = bool(row and check_password_hash(row["password_hash"], password))
    user = ({key: row[key] for key in ("id", "username", "display_name", "role")} if verified else None)
    return {
        "user": user, "rows": rows, "query": query,
        "decision": "authenticated" if verified else "rejected",
        "reason": "pbkdf2_verified" if verified else "invalid_credentials",
        "password_verification_executed": bool(row), "password_verification_result": verified,
        "password_length": len(password),
    }


def create_login_session(user: dict, *, via: str) -> None:
    # Clearing before assignment rotates the signed session payload after secure authentication.
    session.clear()
    session.update({
        "user_id": user["id"], "username": user["username"], "role": user["role"],
        "authenticated_via": via, "login_time": datetime.now(timezone.utc).isoformat(),
    })


def logout_user() -> None:
    session.clear()
