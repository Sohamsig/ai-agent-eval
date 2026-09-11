from list_utils import find_max, remove_duplicates, count_positive


def test_find_max():
    assert find_max([3, 7, 2, 9, 4]) == 9


def test_remove_duplicates():
    assert remove_duplicates([1, 2, 2, 3, 3, 3]) == [1, 2, 3]


def test_count_positive():
    assert count_positive([-2, 4, 7, -1, 0, 5]) == 3