from copy import deepcopy


def deep_merge(base, override):
    """Recursively merge two dictionaries without modifying inputs."""
    if not isinstance(base, dict) or not isinstance(override, dict):
        return None

    result = deepcopy(base)

    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)

    return result


def get_nested(config, path, default=None):
    """Get a nested configuration value using a dot-separated path."""
    if not isinstance(config, dict) or not isinstance(path, str):
        return None

    if not path:
        return default

    current = config

    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return default

        current = current[key]

    return current


def set_nested(config, path, value):
    """Set a nested configuration value using a dot-separated path."""
    if not isinstance(config, dict) or not isinstance(path, str):
        return None

    if not path:
        return None

    keys = path.split(".")
    current = config

    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}

        current = current[key]

    current[keys[-1]] = value

    return config


def remove_nested(config, path):
    """Remove a nested configuration value."""
    if not isinstance(config, dict) or not isinstance(path, str):
        return None

    if not path:
        return None

    keys = path.split(".")
    current = config

    for key in keys[:-1]:
        if not isinstance(current, dict) or key not in current:
            return False

        current = current[key]

    if not isinstance(current, dict) or keys[-1] not in current:
        return False

    del current[keys[-1]]
    return True
