from __future__ import annotations

from datetime import UTC, datetime

from cryptography.fernet import Fernet

from encrypted_cookie_service import (
    demo_encrypted_profile,
    decrypt_demo_profile,
    encrypt_demo_profile,
    tamper_encrypted_token,
)


def test_encrypted_payload_round_trip(app):
    profile = demo_encrypted_profile(datetime.now(UTC))
    token = encrypt_demo_profile(profile, app.config)
    result = decrypt_demo_profile(token, app.config)
    assert result.valid is True
    assert result.profile == profile
    assert result.confidentiality_protected is True
    assert result.integrity_protected is True


def test_encrypted_tokens_use_randomness(app):
    profile = demo_encrypted_profile(datetime.now(UTC))
    assert encrypt_demo_profile(profile, app.config) != encrypt_demo_profile(
        profile, app.config
    )


def test_encrypted_tamper_is_rejected(app):
    token = encrypt_demo_profile(demo_encrypted_profile(datetime.now(UTC)), app.config)
    result = decrypt_demo_profile(tamper_encrypted_token(token), app.config)
    assert result.valid is False
    assert result.encryption_status == "invalid"


def test_encrypted_wrong_key_is_rejected(app):
    token = encrypt_demo_profile(demo_encrypted_profile(datetime.now(UTC)), app.config)
    wrong = dict(app.config)
    wrong["FERNET_KEY"] = Fernet.generate_key().decode("ascii")
    assert decrypt_demo_profile(token, wrong).valid is False


def test_encrypted_profile_has_no_authorization_role():
    profile = demo_encrypted_profile(datetime.now(UTC))
    assert not hasattr(profile, "role")
    assert not hasattr(profile, "session_id")
    assert not hasattr(profile, "password")


def test_encrypted_demo_route_is_read_only_presentation(client):
    response = client.get("/secure/encrypted-demo")
    assert response.status_code == 200
    assert response.headers["X-Lab-Authorization-Used"] == "false"
    cookie = next(
        item
        for item in response.headers.getlist("Set-Cookie")
        if item.startswith("lab06_encrypted_profile=")
    )
    assert "HttpOnly" in cookie
    assert "Authenticated encryption" in response.get_data(as_text=True)

