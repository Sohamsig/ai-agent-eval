from validation_utils import (
    is_valid_email,
    is_valid_phone,
    is_valid_username,
    validate_required_fields,
)


# ============================================================
# EMAIL
# ============================================================

def test_valid_email():
    assert is_valid_email("user@example.com") is True


def test_valid_email_with_subdomain():
    assert is_valid_email("user@mail.example.com") is True


def test_invalid_email_without_at():
    assert is_valid_email("userexample.com") is False


def test_invalid_email_without_domain():
    assert is_valid_email("user@") is False


def test_invalid_email_without_local_part():
    assert is_valid_email("@example.com") is False


def test_invalid_email_with_spaces():
    assert is_valid_email("user name@example.com") is False


def test_invalid_email_non_string():
    assert is_valid_email(None) is False


# ============================================================
# PHONE
# ============================================================

def test_valid_phone():
    assert is_valid_phone("9876543210") is True


def test_valid_phone_with_country_code():
    assert is_valid_phone("+919876543210") is True


def test_invalid_phone_too_short():
    assert is_valid_phone("123456789") is False


def test_invalid_phone_too_long():
    assert is_valid_phone("1234567890123456") is False


def test_invalid_phone_letters():
    assert is_valid_phone("98765abc10") is False


def test_invalid_phone_spaces():
    assert is_valid_phone("98765 43210") is False


def test_invalid_phone_non_string():
    assert is_valid_phone(None) is False


# ============================================================
# USERNAME
# ============================================================

def test_valid_username():
    assert is_valid_username("soham_123") is True


def test_valid_username_letters_only():
    assert is_valid_username("soham") is True


def test_valid_username_numbers():
    assert is_valid_username("user123") is True


def test_username_too_short():
    assert is_valid_username("ab") is False


def test_username_too_long():
    assert is_valid_username("a" * 21) is False


def test_username_with_spaces():
    assert is_valid_username("soham babrekar") is False


def test_username_with_special_character():
    assert is_valid_username("soham@123") is False


def test_username_non_string():
    assert is_valid_username(None) is False


# ============================================================
# REQUIRED FIELDS
# ============================================================

def test_required_fields():
    data = {
        "name": "Soham",
        "email": "soham@example.com",
    }

    assert validate_required_fields(
        data,
        ["name", "email"],
    ) is True


def test_missing_required_field():
    data = {
        "name": "Soham",
    }

    assert validate_required_fields(
        data,
        ["name", "email"],
    ) is False


def test_empty_required_field():
    data = {
        "name": "Soham",
        "email": "",
    }

    assert validate_required_fields(
        data,
        ["name", "email"],
    ) is False


def test_whitespace_required_field():
    data = {
        "name": "Soham",
        "email": "   ",
    }

    assert validate_required_fields(
        data,
        ["name", "email"],
    ) is False


def test_required_fields_does_not_modify_data():
    data = {
        "name": "Soham",
        "email": "soham@example.com",
    }

    original = data.copy()

    result = validate_required_fields(
        data,
        ["name", "email"],
    )

    assert result is True
    assert data == original


def test_invalid_data():
    assert validate_required_fields(
        None,
        ["name"],
    ) is False