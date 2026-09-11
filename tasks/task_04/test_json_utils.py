from json_utils import get_user_name


def test_get_user_name():
    data = {
        "user": {
            "name": "Soham",
            "age": 21
        }
    }

    assert get_user_name(data) == "Soham"