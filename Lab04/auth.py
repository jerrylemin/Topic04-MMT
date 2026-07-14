import time
from functools import wraps

from flask import redirect, request, session, url_for
from werkzeug.security import check_password_hash

from csrf_service import issue_csrf_token
from database import query_one


REAUTH_MAX_AGE_SECONDS = 300


def authenticate(username: str, password: str):
    user = query_one("SELECT * FROM users WHERE username = ?", ((username or "").strip(),))
    return user if user and check_password_hash(user["password_hash"], password or "") else None


def login_user(user) -> None:
    session.clear()
    session.update({
        "user_id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "authenticated_at": time.time(),
        "reauthenticated_at": None,
    })
    issue_csrf_token()


def logout_user() -> None:
    session.clear()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def verify_current_password(password: str | None) -> bool:
    user = query_one("SELECT password_hash FROM users WHERE id = ?", (session.get("user_id"),))
    return bool(user and check_password_hash(user["password_hash"], password or ""))


def mark_reauthenticated() -> None:
    session["reauthenticated_at"] = time.time()


def is_recently_reauthenticated() -> bool:
    timestamp = session.get("reauthenticated_at")
    return bool(timestamp and time.time() - float(timestamp) <= REAUTH_MAX_AGE_SECONDS)


def reauthenticate(current_password: str | None) -> bool:
    if not verify_current_password(current_password):
        return False
    mark_reauthenticated()
    return True
