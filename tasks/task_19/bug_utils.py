def find_max(numbers):
    """Return the maximum number, or None for invalid/empty input."""
    if not isinstance(numbers, (list, tuple)) or not numbers:
        return None

    try:
        return max(numbers)
    except (TypeError, ValueError):
        return None


def divide(a, b):
    """Safely divide a by b."""
    if not isinstance(a, (int, float)) or isinstance(a, bool):
        return None

    if not isinstance(b, (int, float)) or isinstance(b, bool):
        return None

    if b == 0:
        return None

    return a / b


def count_occurrences(items, value):
    """Count how many times value occurs in items."""
    if not isinstance(items, (list, tuple)):
        return 0

    return items.count(value)


def remove_duplicates(items):
    """Remove duplicates while preserving order."""
    if not isinstance(items, (list, tuple)):
        return []

    result = []

    for item in items:
        if item not in result:
            result.append(item)

    return result


def safe_get(data, key, default=None):
    """Safely retrieve a value from a dictionary."""
    if not isinstance(data, dict):
        return default

    return data.get(key, default)