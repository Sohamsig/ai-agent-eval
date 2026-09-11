def set_value(cache, key, value):
    """Store a value in the cache."""
    if not isinstance(cache, dict):
        return False

    if key is None or key == "":
        return False

    cache[key] = value
    return True


def get_value(cache, key, default=None):
    """Return a cached value or default."""
    if not isinstance(cache, dict):
        return default

    return cache.get(key, default)


def delete_value(cache, key):
    """Delete a value from the cache."""
    if not isinstance(cache, dict):
        return False

    if key not in cache:
        return False

    del cache[key]
    return True


def has_key(cache, key):
    """Check whether a key exists in the cache."""
    if not isinstance(cache, dict):
        return False

    return key in cache


def clear_cache(cache):
    """Remove all entries from the cache."""
    if not isinstance(cache, dict):
        return False

    cache.clear()
    return True
