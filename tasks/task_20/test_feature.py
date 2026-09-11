from feature_utils import add_numbers, multiply_numbers
from feature_service import (
    calculate,
    calculate_sum,
    calculate_product,
)


def test_add_numbers():
    assert add_numbers(2, 3) == 5


def test_add_numbers_negative():
    assert add_numbers(-2, 3) == 1


def test_add_numbers_float():
    assert add_numbers(2.5, 1.5) == 4.0


def test_add_numbers_invalid():
    assert add_numbers("2", 3) is None


def test_add_numbers_bool():
    assert add_numbers(True, 3) is None


def test_multiply_numbers():
    assert multiply_numbers(4, 5) == 20


def test_multiply_numbers_negative():
    assert multiply_numbers(-2, 3) == -6


def test_multiply_numbers_float():
    assert multiply_numbers(2.5, 2) == 5.0


def test_multiply_numbers_invalid():
    assert multiply_numbers("4", 5) is None


def test_calculate():
    assert calculate(3, 4) == {
        "sum": 7,
        "product": 12,
    }


def test_calculate_negative():
    assert calculate(-3, 4) == {
        "sum": 1,
        "product": -12,
    }


def test_calculate_invalid():
    assert calculate("3", 4) is None


def test_calculate_sum():
    assert calculate_sum(10, 5) == 15


def test_calculate_product():
    assert calculate_product(10, 5) == 50


def test_calculate_empty_invalid():
    assert calculate(None, 5) is None