from auth_utils import (
    hash_password,
    verify_password,
    generate_token,
    validate_token,
)


def test_hash_password():
    hashed = hash_password("password123")

    assert isinstance(hashed, str)
    assert hashed != "password123"
    assert "password123" not in hashed


def test_hash_password_invalid():
    assert hash_password(None) is None
    assert hash_password("") is None
    assert hash_password(123) is None


def test_hash_password_unique():
    first = hash_password("password123")
    second = hash_password("password123")

    assert first != second


def test_verify_password_correct():
    hashed = hash_password("password123")

    assert verify_password(
        "password123",
        hashed,
    ) is True


def test_verify_password_wrong():
    hashed = hash_password("password123")

    assert verify_password(
        "wrong-password",
        hashed,
    ) is False


def test_verify_password_invalid():
    assert verify_password(
        None,
        "invalid",
    ) is False

    assert verify_password(
        "password",
        None,
    ) is False

    assert verify_password(
        "password",
        "",
    ) is False


def test_generate_token():
    token = generate_token(123)

    assert isinstance(token, str)
    assert token


def test_generate_token_string_id():
    token = generate_token("user-123")

    assert isinstance(token, str)
    assert token


def test_generate_token_invalid():
    assert generate_token(None) is None


def test_validate_token():
    token = generate_token(123)

    assert validate_token(token) == "123"


def test_validate_string_token():
    token = generate_token("user-123")

    assert validate_token(token) == "user-123"


def test_validate_invalid_token():
    assert validate_token(None) is None
    assert validate_token("") is None
    assert validate_token("invalid") is None


def test_validate_tampered_token():
    token = generate_token("user-123")

    payload, signature = token.split(".")

    tampered = payload + "x." + signature

    assert validate_token(tampered) is None