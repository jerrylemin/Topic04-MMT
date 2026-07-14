import pytest

from config import AUTH_LOGIC_INPUT, QUOTE_INPUT, SEARCH_EXPANDED_INPUT
from validation import (ValidationError, input_signals, normalize_spaces, positive_int,
                        validate_keyword, validate_password, validate_username)


@pytest.mark.parametrize("value,expected", [
    ("  Wireless   Mouse  ", "Wireless Mouse"),
    ("USB", "USB"),
    (None, ""),
])
def test_space_normalization(value, expected):
    assert normalize_spaces(value) == expected


@pytest.mark.parametrize("value", ["admin_lab", QUOTE_INPUT, AUTH_LOGIC_INPUT])
def test_vulnerable_username_accepts_normal_and_fixed_scenarios(value):
    assert validate_username(value, vulnerable=True) == value


@pytest.mark.parametrize("value", ["bad name", "x' OR 'x'='x", "a" * 65, ""])
def test_vulnerable_username_rejects_unapproved_or_invalid_values(value):
    with pytest.raises(ValidationError):
        validate_username(value, vulnerable=True)


@pytest.mark.parametrize("value", [QUOTE_INPUT, SEARCH_EXPANDED_INPUT, "USB"])
def test_secure_keyword_treats_sql_shaped_input_as_data(value):
    assert validate_keyword(value, vulnerable=False) == normalize_spaces(value)


@pytest.mark.parametrize("value", [QUOTE_INPUT, SEARCH_EXPANDED_INPUT])
def test_vulnerable_keyword_accepts_only_fixed_sql_scenarios(value):
    assert validate_keyword(value, vulnerable=True) == value


@pytest.mark.parametrize("value", [None, "", " ", "x" * 101])
def test_keyword_rejects_empty_or_oversized_values(value):
    with pytest.raises(ValidationError):
        validate_keyword(value, vulnerable=False)


@pytest.mark.parametrize("value,expected", [("1", 1), (5, 5)])
def test_positive_integer_validation(value, expected):
    assert positive_int(value) == expected


@pytest.mark.parametrize("value", [None, "abc", "0", "-2", "1.2"])
def test_positive_integer_rejects_invalid_values(value):
    with pytest.raises(ValidationError):
        positive_int(value)


@pytest.mark.parametrize("value", [None, "", "x" * 129])
def test_password_length_boundary_rejects_invalid_values(value):
    with pytest.raises(ValidationError):
        validate_password(value)


def test_input_signals_only_detect_defined_local_scenario_markers():
    signals = input_signals(SEARCH_EXPANDED_INPUT)
    assert signals["single_quote_detected"] is True
    assert signals["comment_marker_detected"] is True
    assert signals["boolean_expression_detected"] is True
    assert signals["trust_level"] == "untrusted"

