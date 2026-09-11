from tasks.task_21.text_utils import (
    normalize_text,
    word_count,
    reverse_words,
    is_palindrome,
)


def test_normalize_text():
    assert normalize_text("  Hello World  ") == "hello world"


def test_normalize_text_uppercase():
    assert normalize_text("PYTHON") == "python"


def test_normalize_text_empty():
    assert normalize_text("") == ""


def test_normalize_text_whitespace():
    assert normalize_text("   ") == ""


def test_normalize_text_invalid():
    assert normalize_text(123) is None


def test_word_count():
    assert word_count("hello world") == 2


def test_word_count_multiple_spaces():
    assert word_count("hello   world   python") == 3


def test_word_count_leading_trailing_spaces():
    assert word_count("  hello world  ") == 2


def test_word_count_empty():
    assert word_count("") == 0


def test_word_count_whitespace():
    assert word_count("     ") == 0


def test_word_count_invalid():
    assert word_count(None) is None


def test_reverse_words():
    assert reverse_words("hello world") == "world hello"


def test_reverse_words_multiple():
    assert reverse_words("one two three") == "three two one"


def test_reverse_words_extra_spaces():
    assert reverse_words("  hello   world  ") == "world hello"


def test_reverse_words_empty():
    assert reverse_words("") == ""


def test_reverse_words_invalid():
    assert reverse_words(123) is None


def test_is_palindrome_true():
    assert is_palindrome("madam") is True


def test_is_palindrome_case_insensitive():
    assert is_palindrome("Madam") is True


def test_is_palindrome_with_spaces():
    assert is_palindrome("  Racecar  ") is True


def test_is_palindrome_false():
    assert is_palindrome("hello") is False


def test_is_palindrome_invalid():
    assert is_palindrome(None) is None