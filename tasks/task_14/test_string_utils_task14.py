from tasks.task_14.string_utils import (
    reverse_string,
    is_palindrome,
    count_vowels,
    remove_whitespace,
    capitalize_words,
)


def test_reverse_string():
    assert reverse_string("hello") == "olleh"


def test_reverse_empty_string():
    assert reverse_string("") == ""


def test_reverse_non_string():
    assert reverse_string(None) is None


def test_is_palindrome_true():
    assert is_palindrome("level") is True


def test_is_palindrome_false():
    assert is_palindrome("hello") is False


def test_is_palindrome_case_insensitive():
    assert is_palindrome("Level") is True


def test_is_palindrome_empty():
    assert is_palindrome("") is True


def test_is_palindrome_non_string():
    assert is_palindrome(None) is False


def test_count_vowels():
    assert count_vowels("hello") == 2


def test_count_vowels_uppercase():
    assert count_vowels("AEIOU") == 5


def test_count_vowels_mixed():
    assert count_vowels("Hello World") == 3


def test_count_vowels_empty():
    assert count_vowels("") == 0


def test_count_vowels_non_string():
    assert count_vowels(None) == 0


def test_remove_whitespace():
    assert remove_whitespace("hello world") == "helloworld"


def test_remove_all_whitespace():
    assert remove_whitespace(" h e l l o ") == "hello"


def test_remove_whitespace_empty():
    assert remove_whitespace("") == ""


def test_remove_whitespace_non_string():
    assert remove_whitespace(None) is None


def test_capitalize_words():
    assert capitalize_words("hello world") == "Hello World"


def test_capitalize_multiple_spaces():
    assert capitalize_words("hello   world") == "Hello   World"


def test_capitalize_empty():
    assert capitalize_words("") == ""


def test_capitalize_non_string():
    assert capitalize_words(None) is None