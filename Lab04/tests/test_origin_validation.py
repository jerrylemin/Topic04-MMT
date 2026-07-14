from origin_service import parse_origin, validate_origin_or_referer


def test_origin_is_parsed_and_compared_exactly():
    parsed = parse_origin("http://127.0.0.1:5004")
    assert parsed == {"scheme": "http", "hostname": "127.0.0.1", "port": 5004, "origin": "http://127.0.0.1:5004"}

    allowed = validate_origin_or_referer("http://127.0.0.1:5004", None)
    assert allowed.allowed is True
    assert allowed.source == "origin"
    assert allowed.to_dict() == {
        "origin_raw": "http://127.0.0.1:5004",
        "referer_raw": None,
        "parsed_origin": parsed,
        "parsed_referer": None,
        "expected_origins": tuple(sorted(allowed.expected_origins)),
        "origin_match": True,
        "referer_match": False,
        "decision": "allowed",
        "reason": "origin_allowed",
    }

    assert validate_origin_or_referer("http://127.0.0.1:9004", None).allowed is False
    assert validate_origin_or_referer("http://127.0.0.1:5004.attacker.local", None).allowed is False
    assert validate_origin_or_referer("http://127.0.0.1:5004@attacker.local", None).allowed is False


def test_malformed_origin_is_denied():
    assert validate_origin_or_referer("not an origin", None).allowed is False
    assert validate_origin_or_referer("http://127.0.0.1:5004/path", None).allowed is False
