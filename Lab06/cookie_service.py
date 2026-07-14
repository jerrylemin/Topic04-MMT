from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from flask import Request, Response

from config import LabConfig, cookie_options


PLAIN_USERNAME_COOKIE = "lab06_username"
PLAIN_ROLE_COOKIE = "lab06_role"


@dataclass(frozen=True, slots=True)
class PlainCookieIdentity:
    username: str | None
    role: str | None
    username_present: bool
    role_present: bool


def issue_plain_demo_cookies(
    response: Response, config: LabConfig | Mapping[str, Any] | Any
) -> None:
    options = cookie_options(config, httponly=False)
    response.set_cookie(PLAIN_USERNAME_COOKIE, "student", **options)
    response.set_cookie(PLAIN_ROLE_COOKIE, "user", **options)


def read_plain_identity(request: Request) -> PlainCookieIdentity:
    username = request.cookies.get(PLAIN_USERNAME_COOKIE)
    role = request.cookies.get(PLAIN_ROLE_COOKIE)
    return PlainCookieIdentity(
        username=username,
        role=role,
        username_present=username is not None,
        role_present=role is not None,
    )


def expire_plain_demo_cookies(
    response: Response, config: LabConfig | Mapping[str, Any] | Any
) -> None:
    options = cookie_options(config, httponly=False, max_age=0)
    response.set_cookie(PLAIN_USERNAME_COOKIE, "", expires=0, **options)
    response.set_cookie(PLAIN_ROLE_COOKIE, "", expires=0, **options)
