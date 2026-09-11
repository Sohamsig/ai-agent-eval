def normalize_text(text):
    """Normalize text by trimming whitespace and converting to lowercase."""
    if not isinstance(text, str):
        return None

    return text.strip().lower()


def word_count(text):
    """Return the number of words in text."""
    if not isinstance(text, str):
        return None

    return len(text.split())


def reverse_words(text):
    """Reverse the order of words in text."""
    if not isinstance(text, str):
        return None

    return " ".join(text.split()[::-1])


def is_palindrome(text):
    """Return True if text is a palindrome, ignoring case and outer whitespace."""
    if not isinstance(text, str):
        return None

    cleaned = text.strip().lower()
    return cleaned == cleaned[::-1]