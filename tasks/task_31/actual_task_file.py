def normalize_email(email):
    if not isinstance(email, str):
        return None

    email = email.strip().lower()

    if not email:
        return None

    return email


def is_valid_email(email):
    email = normalize_email(email)

    if email is None:
        return False

    if "@" not in email:
        return False

    local, domain = email.split("@", 1)

    if not local or not domain:
        return False

    if "." not in domain:
        return False

    return True


def create_user(email, name):
    normalized_email = normalize_email(email)

    if normalized_email is None:
        return None

    if not is_valid_email(normalized_email):
        return None

    if not isinstance(name, str):
        return None

    name = name.strip()

    if not name:
        return None

    return {
        "email": normalized_email,
        "name": name,
    }
