from cache_utils import get, set, delete, clear, contains


def test_set_and_get():
    clear()

    set("name", "Soham")

    assert get("name") == "Soham"


def test_get_missing_key():
    clear()

    assert get("missing") is None


def test_get_missing_key_with_default():
    clear()

    assert get("missing", "default") == "default"


def test_set_overwrites_existing_value():
    clear()

    set("count", 1)
    set("count", 2)

    assert get("count") == 2


def test_contains_existing_key():
    clear()

    set("key", "value")

    assert contains("key") is True


def test_contains_missing_key():
    clear()

    assert contains("missing") is False


def test_delete_existing_key():
    clear()

    set("key", "value")

    assert delete("key") is True
    assert get("key") is None


def test_delete_missing_key():
    clear()

    assert delete("missing") is False


def test_clear():
    set("a", 1)
    set("b", 2)

    clear()

    assert get("a") is None
    assert get("b") is None
    assert contains("a") is False
    assert contains("b") is False


def test_empty_string_key():
    clear()

    set("", "value")

    assert get("") == "value"
    assert contains("") is True


def test_none_value():
    clear()

    set("key", None)

    assert get("key") is None
    assert contains("key") is True