_CACHE = {}


def get(key, default=None):
    """Return the cached value or default if the key is missing."""
    return _CACHE.get(key, default)


def set(key, value):
    """Store a value in the cache."""
    _CACHE[key] = value


def delete(key):
    """Delete a key from the cache.

    Returns True when the key existed and was deleted,
    otherwise False.
    """
    if key in _CACHE:
        del _CACHE[key]
        return True

    return False


def clear():
    """Remove all values from the cache."""
    _CACHE.clear()


def contains(key):
    """Return True if the cache contains the key."""
    return key in _CACHE