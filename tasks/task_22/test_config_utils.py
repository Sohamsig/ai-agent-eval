import pytest

from tasks.task_22.config_utils import (
    deep_merge,
    get_nested,
    set_nested,
    remove_nested,
)


# -------------------------
# deep_merge
# -------------------------

def test_deep_merge_basic():
    base = {"a": 1, "b": 2}
    override = {"b": 3, "c": 4}

    result = deep_merge(base, override)

    assert result == {"a": 1, "b": 3, "c": 4}


def test_deep_merge_nested():
    base = {
        "database": {
            "host": "localhost",
            "port": 5432,
        }
    }

    override = {
        "database": {
            "port": 5433,
            "name": "app",
        }
    }

    result = deep_merge(base, override)

    assert result == {
        "database": {
            "host": "localhost",
            "port": 5433,
            "name": "app",
        }
    }


def test_deep_merge_does_not_modify_base():
    base = {"a": 1, "nested": {"x": 10}}
    override = {"b": 2}

    result = deep_merge(base, override)

    assert base == {"a": 1, "nested": {"x": 10}}
    assert result == {"a": 1, "nested": {"x": 10}, "b": 2}


def test_deep_merge_does_not_modify_override():
    base = {"a": 1}
    override = {"nested": {"x": 10}}

    result = deep_merge(base, override)

    result["nested"]["x"] = 99

    assert override == {"nested": {"x": 10}}


def test_deep_merge_empty_dicts():
    assert deep_merge({}, {}) == {}


def test_deep_merge_invalid_base():
    assert deep_merge(None, {"a": 1}) is None


def test_deep_merge_invalid_override():
    assert deep_merge({"a": 1}, None) is None


# -------------------------
# get_nested
# -------------------------

def test_get_nested_value():
    config = {
        "database": {
            "host": "localhost",
            "port": 5432,
        }
    }

    assert get_nested(config, "database.host") == "localhost"


def test_get_nested_deep_value():
    config = {
        "app": {
            "database": {
                "connection": {
                    "timeout": 30
                }
            }
        }
    }

    assert get_nested(
        config,
        "app.database.connection.timeout"
    ) == 30


def test_get_nested_missing_key():
    config = {"database": {"host": "localhost"}}

    assert get_nested(config, "database.port", 5432) == 5432


def test_get_nested_missing_intermediate():
    config = {"database": None}

    assert get_nested(config, "database.host", "default") == "default"


def test_get_nested_empty_path():
    config = {"a": 1}

    assert get_nested(config, "", "default") == "default"


def test_get_nested_invalid_config():
    assert get_nested(None, "a.b", "default") is None


def test_get_nested_invalid_path():
    assert get_nested({"a": 1}, None, "default") is None


# -------------------------
# set_nested
# -------------------------

def test_set_nested_existing_path():
    config = {
        "database": {
            "host": "localhost"
        }
    }

    result = set_nested(config, "database.host", "127.0.0.1")

    assert result is config
    assert config["database"]["host"] == "127.0.0.1"


def test_set_nested_create_path():
    config = {}

    set_nested(config, "database.host", "localhost")

    assert config == {
        "database": {
            "host": "localhost"
        }
    }


def test_set_nested_deep_path():
    config = {}

    set_nested(config, "app.database.timeout", 30)

    assert config == {
        "app": {
            "database": {
                "timeout": 30
            }
        }
    }


def test_set_nested_empty_path():
    config = {}

    assert set_nested(config, "", 10) is None
    assert config == {}


def test_set_nested_invalid_config():
    assert set_nested(None, "a.b", 10) is None


# -------------------------
# remove_nested
# -------------------------

def test_remove_nested_existing_value():
    config = {
        "database": {
            "host": "localhost",
            "port": 5432,
        }
    }

    assert remove_nested(config, "database.port") is True

    assert config == {
        "database": {
            "host": "localhost"
        }
    }


def test_remove_nested_missing_value():
    config = {
        "database": {
            "host": "localhost"
        }
    }

    assert remove_nested(config, "database.port") is False


def test_remove_nested_missing_intermediate():
    config = {
        "database": None
    }

    assert remove_nested(config, "database.port") is False


def test_remove_nested_empty_path():
    config = {"a": 1}

    assert remove_nested(config, "") is None


def test_remove_nested_invalid_config():
    assert remove_nested(None, "a.b") is None


def test_remove_nested_invalid_path():
    assert remove_nested({"a": 1}, None) is None