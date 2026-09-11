from actual_task_file import normalize_email, is_valid_email, create_user


# Existing tests — preserved
def test_normalize_email():
    assert normalize_email(" TEST@Example.COM ") == "test@example.com"


def test_valid_email():
    assert is_valid_email("user@example.com") is True


def test_invalid_email():
    assert is_valid_email("invalid-email") is False


def test_create_user():
    result = create_user(" TEST@example.com ", "Soham")

    assert result == {
        "email": "test@example.com",
        "name": "Soham",
    }


def test_invalid_user():
    assert create_user("invalid", "Soham") is None


# Additional meaningful coverage
def test_normalize_email_empty_string():
    assert normalize_email("") is None


def test_normalize_email_whitespace_only():
    assert normalize_email("   ") is None


def test_normalize_email_non_string():
    assert normalize_email(None) is None
    assert normalize_email(123) is None


def test_is_valid_email_missing_local_part():
    assert is_valid_email("@example.com") is False


def test_is_valid_email_missing_domain():
    assert is_valid_email("user@") is False


def test_is_valid_email_domain_without_dot():
    assert is_valid_email("user@example") is False


def test_is_valid_email_non_string():
    assert is_valid_email(None) is False
    assert is_valid_email(123) is False


def test_is_valid_email_boundary():
    assert is_valid_email("a@b.c") is True


def test_create_user_trims_name():
    result = create_user("user@example.com", "  Soham  ")

    assert result["name"] == "Soham"


def test_create_user_rejects_non_string_email():
    assert create_user(None, "Soham") is None


def test_create_user_rejects_non_string_name():
    assert create_user("user@example.com", None) is None
    assert create_user("user@example.com", 123) is None


def test_create_user_rejects_empty_name():
    assert create_user("user@example.com", "") is None


def test_create_user_rejects_whitespace_name():
    assert create_user("user@example.com", "   ") is None


def test_create_user_boundary_email_and_name():
    result = create_user("a@b.c", "A")

    assert result == {
        "email": "a@b.c",
        "name": "A",
    }


def test_create_user_normalizes_email_and_name_together():
    result = create_user("  USER@EXAMPLE.COM  ", "  Soham  ")

    assert result == {
        "email": "user@example.com",
        "name": "Soham",
    }
