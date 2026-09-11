import re


def is_valid_email(email):
    """Return True if email has a basic valid email format."""
    if not isinstance(email, str):
        return False

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    """Return True for a 10-digit phone or +91 followed by 10 digits."""
    if not isinstance(phone, str):
        return False

    return re.fullmatch(r"\d{10}", phone) is not None or \
           re.fullmatch(r"\+91\d{10}", phone) is not None


def is_valid_username(username):
    """Return True for usernames containing 3-20 letters, digits, or underscores."""
    if not isinstance(username, str):
        return False

    return re.fullmatch(r"[A-Za-z0-9_]{3,20}", username) is not None


def validate_required_fields(data, fields):
    """Return True when all required fields exist and are non-empty."""
    if not isinstance(data, dict):
        return False

    for field in fields:
        if field not in data:
            return False

        value = data[field]

        if value is None:
            return False

        if isinstance(value, str) and not value.strip():
            return False

    return True