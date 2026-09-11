from actual_task_file import normalize_email, is_valid_email, create_user


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
