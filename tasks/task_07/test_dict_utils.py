from dict_utils import get_value, merge_dicts, filter_by_value


def test_get_value():
    data = {"name": "Soham", "age": 21}

    assert get_value(data, "name") == "Soham"
    assert get_value(data, "missing") is None
    assert get_value(data, "missing", "default") == "default"


def test_merge_dicts():
    first = {"a": 1, "b": 2}
    second = {"b": 3, "c": 4}

    assert merge_dicts(first, second) == {
        "a": 1,
        "b": 3,
        "c": 4,
    }


def test_filter_by_value():
    data = {
        "a": 10,
        "b": 5,
        "c": 20,
    }

    assert filter_by_value(data, 10) == {
        "a": 10,
        "c": 20,
    }