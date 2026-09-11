from text_utils import normalize_text, count_words, reverse_words


def test_normalize_text():
    assert normalize_text("  Hello   WORLD  ") == "hello world"


def test_count_words():
    assert count_words("hello world from python") == 4


def test_reverse_words():
    assert reverse_words("hello world python") == "python world hello"