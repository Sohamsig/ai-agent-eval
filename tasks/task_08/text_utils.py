def normalize_text(text):
    """
    Normalize a string by:
    - removing leading/trailing whitespace
    - converting to lowercase
    - collapsing consecutive whitespace into one space
    - preserving punctuation
    """
    return " ".join(text.strip().lower().split())


def count_words(text):
    """
    Return the number of words in the text.
    """
    return len(text.split())


def reverse_words(text):
    """
    Return the words in reverse order.
    """
    return " ".join(text.split()[::-1])
