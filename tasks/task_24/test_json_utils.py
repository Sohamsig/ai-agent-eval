import json
import pytest

from tasks.task_24.actual_task_file import (
    serialize_data,
    deserialize_data,
    get_json_value,
    set_json_value,
    remove_json_value,
)


# ---------------------------------------------------------
# serialize_data
# ---------------------------------------------------------

def test_serialize_dict():
    data = {"name": "Alice", "age": 25}

    result = serialize_data(data)

    assert isinstance(result, str)
    assert json.loads(result) == data


def test_serialize_list():
    data = [1, 2, 3, "hello"]

    result = serialize_data(data)

    assert isinstance(result, str)
    assert json.loads(result) == data


def test_serialize_nested_data():
    data = {
        "user": {
            "name": "Alice",
            "skills": ["Python", "Go"],
            "active": True,
        }
    }

    result = serialize_data(data)

    assert json.loads(result) == data


def test_serialize_none():
    result = serialize_data(None)

    assert result == "null"


def test_serialize_boolean():
    assert json.loads(serialize_data(True)) is True
    assert json.loads(serialize_data(False)) is False


def test_serialize_numbers():
    assert json.loads(serialize_data(42)) == 42
    assert json.loads(serialize_data(3.14)) == 3.14


# ---------------------------------------------------------
# deserialize_data
# ---------------------------------------------------------

def test_deserialize_dict():
    data = '{"name": "Alice", "age": 25}'

    result = deserialize_data(data)

    assert result == {
        "name": "Alice",
        "age": 25,
    }


def test_deserialize_list():
    result = deserialize_data('[1, 2, 3]')

    assert result == [1, 2, 3]


def test_deserialize_nested_data():
    data = """
    {
        "user": {
            "name": "Alice",
            "skills": ["Python", "Go"]
        }
    }
    """

    result = deserialize_data(data)

    assert result["user"]["name"] == "Alice"
    assert result["user"]["skills"] == ["Python", "Go"]


def test_deserialize_boolean():
    assert deserialize_data("true") is True
    assert deserialize_data("false") is False


def test_deserialize_null():
    assert deserialize_data("null") is None


def test_deserialize_invalid_json():
    with pytest.raises(ValueError):
        deserialize_data('{"name": "Alice"')


# ---------------------------------------------------------
# get_json_value
# ---------------------------------------------------------

def test_get_top_level_value():
    data = {
        "name": "Alice",
        "age": 25,
    }

    assert get_json_value(data, "name") == "Alice"


def test_get_nested_value():
    data = {
        "user": {
            "name": "Alice",
            "age": 25,
        }
    }

    assert get_json_value(data, "user.name") == "Alice"


def test_get_deep_nested_value():
    data = {
        "user": {
            "profile": {
                "address": {
                    "city": "Pune"
                }
            }
        }
    }

    assert get_json_value(
        data,
        "user.profile.address.city"
    ) == "Pune"


def test_get_missing_value():
    data = {
        "user": {
            "name": "Alice"
        }
    }

    assert get_json_value(
        data,
        "user.age"
    ) is None


def test_get_missing_value_with_default():
    data = {
        "user": {
            "name": "Alice"
        }
    }

    assert get_json_value(
        data,
        "user.age",
        100
    ) == 100


def test_get_missing_intermediate_value():
    data = {
        "user": None
    }

    assert get_json_value(
        data,
        "user.profile.name",
        "unknown"
    ) == "unknown"


def test_get_nested_missing_key():
    data = {
        "user": {
            "profile": {}
        }
    }

    assert get_json_value(
        data,
        "user.profile.name",
        "unknown"
    ) == "unknown"


# ---------------------------------------------------------
# set_json_value
# ---------------------------------------------------------

def test_set_top_level_value():
    data = {
        "name": "Alice"
    }

    result = set_json_value(
        data,
        "name",
        "Bob"
    )

    assert result is data
    assert data["name"] == "Bob"


def test_set_nested_existing_path():
    data = {
        "user": {
            "name": "Alice"
        }
    }

    set_json_value(
        data,
        "user.name",
        "Bob"
    )

    assert data == {
        "user": {
            "name": "Bob"
        }
    }


def test_set_nested_create_path():
    data = {}

    set_json_value(
        data,
        "user.name",
        "Alice"
    )

    assert data == {
        "user": {
            "name": "Alice"
        }
    }


def test_set_deep_nested_create_path():
    data = {}

    set_json_value(
        data,
        "user.profile.address.city",
        "Pune"
    )

    assert data == {
        "user": {
            "profile": {
                "address": {
                    "city": "Pune"
                }
            }
        }
    }


def test_set_preserves_existing_values():
    data = {
        "user": {
            "name": "Alice",
            "age": 25,
        }
    }

    set_json_value(
        data,
        "user.name",
        "Bob"
    )

    assert data["user"]["name"] == "Bob"
    assert data["user"]["age"] == 25


def test_set_nested_returns_same_object():
    data = {}

    result = set_json_value(
        data,
        "user.name",
        "Alice"
    )

    assert result is data


# ---------------------------------------------------------
# remove_json_value
# ---------------------------------------------------------

def test_remove_top_level_value():
    data = {
        "name": "Alice",
        "age": 25,
    }

    result = remove_json_value(
        data,
        "age"
    )

    assert result is True
    assert data == {
        "name": "Alice"
    }


def test_remove_nested_value():
    data = {
        "user": {
            "name": "Alice",
            "age": 25,
        }
    }

    result = remove_json_value(
        data,
        "user.age"
    )

    assert result is True
    assert data == {
        "user": {
            "name": "Alice"
        }
    }


def test_remove_deep_nested_value():
    data = {
        "user": {
            "profile": {
                "name": "Alice",
                "age": 25,
            }
        }
    }

    result = remove_json_value(
        data,
        "user.profile.age"
    )

    assert result is True
    assert data == {
        "user": {
            "profile": {
                "name": "Alice"
            }
        }
    }


def test_remove_missing_value():
    data = {
        "user": {
            "name": "Alice"
        }
    }

    result = remove_json_value(
        data,
        "user.age"
    )

    assert result is False

    assert data == {
        "user": {
            "name": "Alice"
        }
    }


def test_remove_missing_intermediate():
    data = {
        "user": {
            "name": "Alice"
        }
    }

    result = remove_json_value(
        data,
        "user.profile.age"
    )

    assert result is False


def test_remove_does_not_remove_parent():
    data = {
        "user": {
            "profile": {
                "name": "Alice"
            }
        }
    }

    result = remove_json_value(
        data,
        "user.profile.age"
    )

    assert result is False

    assert data == {
        "user": {
            "profile": {
                "name": "Alice"
            }
        }
    }