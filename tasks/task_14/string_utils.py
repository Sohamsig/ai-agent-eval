def reverse_string(value):
    """Return the reversed string, or None for non-string input."""
    if not isinstance(value, str):
        return None

    return value[::-1]


def is_palindrome(value):
    """Return True if the string is a palindrome, ignoring case."""
    if not isinstance(value, str):
        return False

    normalized = value.lower()
    return normalized == normalized[::-1]


def count_vowels(value):
    """Count vowels in a string. Return 0 for non-string input."""
    if not isinstance(value, str):
        return 0

    return sum(1 for char in value if char.lower() in "aeiou")


def remove_whitespace(value):
    """Remove all whitespace characters from a string."""
    if not isinstance(value, str):
        return None

    return "".join(value.split())


def capitalize_words(value):
    """Capitalize the first letter of each word while preserving spacing."""
    if not isinstance(value, str):
        return None

    if value == "":
        return ""

    return " ".join(
        word.capitalize()
        for word in value.split(" ")
    )