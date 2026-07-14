from functools import wraps

from flask import redirect, request, session, url_for
from werkzeug.security import check_password_hash

from database import query_one


def authenticate(username: str, password: str):
    user = query_one("SELECT * FROM users WHERE username = ?", ((username or "").strip(),))
    return user if user and check_password_hash(user["password_hash"], password or "") else None


def login_user(user) -> None:
    session.clear()
    session.update(user_id=user["id"], username=user["username"], role=user["role"], lab_mode="secure")


def logout_user() -> None:
    session.clear()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.full_path.rstrip("?")))
        return view(*args, **kwargs)

    return wrapped

