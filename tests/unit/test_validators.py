from reusable_library.validators import (
    validate_date,
    validate_email,
    validate_password,
    validate_required,
)


def test_validate_required_accepts_non_empty_value():
    assert validate_required("John Doe") is True


def test_validate_required_rejects_empty_value():
    assert validate_required("") is False


def test_validate_required_rejects_whitespace():
    assert validate_required("   ") is False


def test_validate_email_accepts_valid_email():
    assert validate_email("john@test.com") is True


def test_validate_email_rejects_invalid_email():
    assert validate_email("john@test") is False


def test_validate_password_accepts_password_of_minimum_length():
    assert validate_password("1234") is True


def test_validate_password_rejects_short_password():
    assert validate_password("123") is False


def test_validate_date_accepts_valid_date():
    assert validate_date("2026-11-20") is True


def test_validate_date_rejects_invalid_date():
    assert validate_date("20-11-2026") is False