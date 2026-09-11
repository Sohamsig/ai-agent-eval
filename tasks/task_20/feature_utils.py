def add_numbers(a, b):
    """Return the sum of two numbers."""
    if isinstance(a, bool) or isinstance(b, bool):
        return None

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return None

    return a + b


def multiply_numbers(a, b):
    """Return the product of two numbers."""
    if isinstance(a, bool) or isinstance(b, bool):
        return None

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return None

    return a * b