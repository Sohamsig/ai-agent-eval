def get_config(config, key, default=None):
    """Return a configuration value or the default if the key is missing."""
    return config.get(key, default)


def set_config(config, key, value):
    """Set a configuration value and return the updated config."""
    config[key] = value
    return config


def merge_configs(base, override):
    """Return a new config containing values from both dictionaries.

    Values from override take precedence over values from base.
    """
    result = base.copy()
    result.update(override)
    return result


def remove_config(config, key):
    """Remove a key from the configuration and return the updated config."""
    config.pop(key, None)
    return config