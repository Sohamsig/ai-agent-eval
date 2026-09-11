from bug_utils import (
    find_max,
    divide,
    count_occurrences,
    remove_duplicates,
    safe_get,
)


def test_find_max():
    assert find_max([1, 5, 3, 2]) == 5


def test_find_max_negative():
    assert find_max([-5, -2, -10]) == -2


def test_find_max_empty():
    assert find_max([]) is None


def test_find_max_invalid():
    assert find_max(None) is None


def test_divide():
    assert divide(10, 2) == 5


def test_divide_float():
    assert divide(5, 2) == 2.5


def test_divide_by_zero():
    assert divide(10, 0) is None


def test_divide_invalid():
    assert divide("10", 2) is None


def test_count_occurrences():
    assert count_occurrences([1, 2, 2, 3, 2], 2) == 3


def test_count_occurrences_missing():
    assert count_occurrences([1, 2, 3], 5) == 0


def test_count_occurrences_invalid():
    assert count_occurrences(None, 1) == 0


def test_remove_duplicates():
    assert remove_duplicates([1, 2, 2, 3, 1]) == [1, 2, 3]


def test_remove_duplicates_preserves_order():
    assert remove_duplicates(["b", "a", "b", "c"]) == ["b", "a", "c"]


def test_remove_duplicates_empty():
    assert remove_duplicates([]) == []


def test_remove_duplicates_invalid():
    assert remove_duplicates(None) == []


def test_safe_get():
    assert safe_get({"name": "Soham"}, "name") == "Soham"


def test_safe_get_missing():
    assert safe_get({"name": "Soham"}, "age") is None


def test_safe_get_default():
    assert safe_get({}, "age", 20) == 20


def test_safe_get_invalid():
    assert safe_get(None, "name", "unknown") == "unknown"