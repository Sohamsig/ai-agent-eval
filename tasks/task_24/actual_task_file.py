import json


def serialize_data(data):
    return json.dumps(data)


def deserialize_data(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON") from exc


def get_json_value(data, path, default=None):
    current = data

    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return default

        current = current[key]

    return current


def set_json_value(data, path, value):
    keys = path.split(".")
    current = data

    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}

        current = current[key]

    current[keys[-1]] = value

    # Important: return the same object
    return data


def remove_json_value(data, path):
    keys = path.split(".")
    current = data

    for key in keys[:-1]:
        if not isinstance(current, dict) or key not in current:
            return False

        current = current[key]

    if not isinstance(current, dict) or keys[-1] not in current:
        return False

    del current[keys[-1]]
    return True