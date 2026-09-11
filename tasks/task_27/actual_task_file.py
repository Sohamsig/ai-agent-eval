"""
Task 27 - User Data Utilities
"""


def get_user_name(user):
    if not isinstance(user, dict):
        return None

    if "name" not in user:
        return None

    name = user["name"]

    if not isinstance(name, str):
        return None

    return name.strip()


def get_user_email(user):
    if not isinstance(user, dict):
        return None

    if "email" not in user:
        return None

    email = user["email"]

    if not isinstance(email, str):
        return None

    return email.strip().lower()


def get_user_age(user):
    if not isinstance(user, dict):
        return None

    if "age" not in user:
        return None

    age = user["age"]

    # bool is a subclass of int, so explicitly reject bool.
    if not isinstance(age, int) or isinstance(age, bool):
        return None

    if age < 0:
        return None

    return age


def format_user(user):
    if not isinstance(user, dict):
        return ""

    name = None
    email = None
    age = None

    if "name" in user:
        if isinstance(user["name"], str):
            name = user["name"].strip()

    if "email" in user:
        if isinstance(user["email"], str):
            email = user["email"].strip().lower()

    if "age" in user:
        if isinstance(user["age"], int) and not isinstance(user["age"], bool):
            if user["age"] >= 0:
                age = user["age"]

    parts = []

    if name is not None:
        parts.append(name)

    if email is not None:
        parts.append(email)

    if age is not None:
        parts.append(str(age))

    return ", ".join(parts)


def filter_users(users, min_age=None):
    if not isinstance(users, list):
        return []

    result = []

    for user in users:
        if not isinstance(user, dict):
            continue

        if min_age is not None:
            if not isinstance(min_age, int) or isinstance(min_age, bool):
                continue

            if "age" not in user:
                continue

            if not isinstance(user["age"], int) or isinstance(user["age"], bool):
                continue

            if user["age"] < min_age:
                continue

        result.append(user)

    return result
