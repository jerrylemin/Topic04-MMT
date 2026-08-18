from origin_service import validate_origin_or_referer


def test_referer_is_strict_fallback_only_when_origin_missing():
    assert validate_origin_or_referer(None, "http://localhost:5004/secure/change-email").allowed
    assert not validate_origin_or_referer(None, "http://localhost:9004/attack").allowed
    assert not validate_origin_or_referer(None, None).allowed
    assert not validate_origin_or_referer(
        "http://127.0.0.1:9004", "http://127.0.0.1:5004/secure/change-email"
    ).allowed
