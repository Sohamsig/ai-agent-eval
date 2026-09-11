import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parent / "actual_task_file.py"

spec = importlib.util.spec_from_file_location(
    "actual_task_file",
    MODULE_PATH
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


get_user_name = module.get_user_name
get_user_email = module.get_user_email
get_user_age = module.get_user_age
format_user = module.format_user
filter_users = module.filter_users


def test_get_user_name():
    assert get_user_name({"name": " Alice "}) == "Alice"


def test_get_user_name_missing():
    assert get_user_name({}) is None


def test_get_user_name_invalid():
    assert get_user_name({"name": 123}) is None


def test_get_user_email():
    assert get_user_email({"email": " ALICE@EXAMPLE.COM "}) == "alice@example.com"


def test_get_user_email_missing():
    assert get_user_email({}) is None


def test_get_user_email_invalid():
    assert get_user_email({"email": 123}) is None


def test_get_user_age():
    assert get_user_age({"age": 25}) == 25


def test_get_user_age_negative():
    assert get_user_age({"age": -1}) is None


def test_get_user_age_invalid():
    assert get_user_age({"age": "25"}) is None


def test_get_user_age_bool():
    assert get_user_age({"age": True}) is None


def test_format_user_all_fields():
    user = {
        "name": " Alice ",
        "email": " ALICE@EXAMPLE.COM ",
        "age": 25,
    }

    assert format_user(user) == "Alice, alice@example.com, 25"


def test_format_user_name_only():
    assert format_user({"name": " Alice "}) == "Alice"


def test_format_user_email_only():
    assert format_user({"email": " TEST@EXAMPLE.COM "}) == "test@example.com"


def test_format_user_age_only():
    assert format_user({"age": 30}) == "30"


def test_format_user_empty():
    assert format_user({}) == ""


def test_format_user_invalid():
    assert format_user(None) == ""


def test_filter_users():
    users = [
        {"name": "A", "age": 20},
        {"name": "B", "age": 30},
        {"name": "C", "age": 40},
    ]

    assert filter_users(users, 30) == [
        {"name": "B", "age": 30},
        {"name": "C", "age": 40},
    ]


def test_filter_users_without_min_age():
    users = [
        {"name": "A"},
        {"name": "B"},
    ]

    assert filter_users(users) == users


def test_filter_users_empty():
    assert filter_users([]) == []


def test_filter_users_invalid_input():
    assert filter_users(None) == []


def test_filter_users_invalid_users():
    users = [
        {"name": "A", "age": 20},
        None,
        "invalid",
        {"name": "B", "age": 30},
    ]

    assert filter_users(users, 20) == [
        {"name": "A", "age": 20},
        {"name": "B", "age": 30},
    ]


def test_filter_users_min_age_zero():
    users = [
        {"name": "A", "age": 0},
        {"name": "B", "age": 10},
    ]

    assert filter_users(users, 0) == users


def test_filter_users_invalid_min_age():
    users = [
        {"name": "A", "age": 20},
    ]

    assert filter_users(users, "20") == []


def test_original_user_objects_are_preserved():
    user = {"name": "A", "age": 20}
    users = [user]

    result = filter_users(users)

    assert result[0] is user


def test_format_user_does_not_modify_input():
    user = {
        "name": " Alice ",
        "email": " TEST@EXAMPLE.COM ",
        "age": 25,
    }

    original = user.copy()

    format_user(user)

    assert user == original


def test_functions_have_same_public_names():
    assert callable(get_user_name)
    assert callable(get_user_email)
    assert callable(get_user_age)
    assert callable(format_user)
    assert callable(filter_users)
