from tasks.task_22.cache_utils import (
    set_value,
    get_value,
    delete_value,
    has_key,
    clear_cache,
)


def test_set_value():
    cache = {}

    assert set_value(cache, "name", "Soham") is True
    assert cache["name"] == "Soham"


def test_set_value_integer():
    cache = {}

    assert set_value(cache, "age", 21) is True
    assert cache["age"] == 21


def test_set_value_none():
    cache = {}

    assert set_value(cache, "value", None) is True
    assert "value" in cache
    assert cache["value"] is None


def test_set_value_boolean():
    cache = {}

    assert set_value(cache, "active", True) is True
    assert cache["active"] is True


def test_set_value_invalid_cache():
    assert set_value([], "name", "Soham") is False
    assert set_value(None, "name", "Soham") is False


def test_set_value_invalid_key():
    cache = {}

    assert set_value(cache, "", "value") is False
    assert set_value(cache, None, "value") is False


def test_get_value():
    cache = {"name": "Soham"}

    assert get_value(cache, "name") == "Soham"


def test_get_value_missing():
    cache = {"name": "Soham"}

    assert get_value(cache, "age") is None
    assert get_value(cache, "age", 21) == 21


def test_get_value_none_value():
    cache = {"value": None}

    assert get_value(cache, "value", "default") is None


def test_get_value_invalid_input():
    assert get_value(None, "name") is None
    assert get_value([], "name", "default") == "default"
    assert get_value({}, "") is None


def test_delete_value():
    cache = {"name": "Soham"}

    assert delete_value(cache, "name") is True
    assert "name" not in cache


def test_delete_missing_value():
    cache = {"name": "Soham"}

    assert delete_value(cache, "age") is False


def test_delete_invalid_input():
    assert delete_value(None, "name") is False
    assert delete_value([], "name") is False
    assert delete_value({}, "") is False


def test_has_key():
    cache = {"name": "Soham"}

    assert has_key(cache, "name") is True
    assert has_key(cache, "age") is False


def test_has_key_invalid_input():
    assert has_key(None, "name") is False
    assert has_key([], "name") is False
    assert has_key({}, "") is False


def test_clear_cache():
    cache = {
        "name": "Soham",
        "age": 21,
        "active": True,
    }

    result = clear_cache(cache)

    assert result is True
    assert cache == {}


def test_clear_cache_preserves_object():
    cache = {"name": "Soham"}
    original_cache = cache

    clear_cache(cache)

    assert cache is original_cache
    assert cache == {}


def test_clear_invalid_cache():
    assert clear_cache(None) is False
    assert clear_cache([]) is False
    assert clear_cache("cache") is False
