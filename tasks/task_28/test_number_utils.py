import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parent / "actual_task_file.py"

spec = importlib.util.spec_from_file_location(
    "actual_task_file",
    MODULE_PATH
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


is_even = module.is_even
is_prime = module.is_prime
factorial = module.factorial
fibonacci = module.fibonacci
sum_of_digits = module.sum_of_digits


# ============================================================
# is_even
# ============================================================

def test_is_even():
    assert is_even(2) is True


def test_is_even_odd():
    assert is_even(3) is False


def test_is_even_zero():
    assert is_even(0) is True


def test_is_even_negative_even():
    assert is_even(-2) is True


def test_is_even_negative_odd():
    assert is_even(-3) is False


def test_is_even_string():
    assert is_even("2") is False


def test_is_even_none():
    assert is_even(None) is False


def test_is_even_float():
    assert is_even(2.0) is False


def test_is_even_boolean():
    assert is_even(True) is False


# ============================================================
# is_prime
# ============================================================

def test_is_prime():
    assert is_prime(7) is True


def test_is_not_prime():
    assert is_prime(9) is False


def test_is_prime_two():
    assert is_prime(2) is True


def test_is_prime_three():
    assert is_prime(3) is True


def test_is_prime_one():
    assert is_prime(1) is False


def test_is_prime_zero():
    assert is_prime(0) is False


def test_is_prime_negative():
    assert is_prime(-7) is False


def test_is_prime_even_composite():
    assert is_prime(4) is False


def test_is_prime_odd_composite():
    assert is_prime(15) is False


def test_is_prime_larger_prime():
    assert is_prime(97) is True


def test_is_prime_larger_composite():
    assert is_prime(100) is False


def test_is_prime_string():
    assert is_prime("7") is False


def test_is_prime_none():
    assert is_prime(None) is False


def test_is_prime_boolean():
    assert is_prime(True) is False


# ============================================================
# factorial
# ============================================================

def test_factorial():
    assert factorial(5) == 120


def test_factorial_zero():
    assert factorial(0) == 1


def test_factorial_one():
    assert factorial(1) == 1


def test_factorial_three():
    assert factorial(3) == 6


def test_factorial_larger_value():
    assert factorial(10) == 3628800


def test_factorial_negative():
    assert factorial(-1) is None


def test_factorial_string():
    assert factorial("5") is None


def test_factorial_float():
    assert factorial(5.0) is None


def test_factorial_boolean():
    assert factorial(True) is None


# ============================================================
# fibonacci
# ============================================================

def test_fibonacci():
    assert fibonacci(6) == 8


def test_fibonacci_zero():
    assert fibonacci(0) == 0


def test_fibonacci_one():
    assert fibonacci(1) == 1


def test_fibonacci_two():
    assert fibonacci(2) == 1


def test_fibonacci_three():
    assert fibonacci(3) == 2


def test_fibonacci_ten():
    assert fibonacci(10) == 55


def test_fibonacci_larger_value():
    assert fibonacci(20) == 6765


def test_fibonacci_negative():
    assert fibonacci(-1) is None


def test_fibonacci_string():
    assert fibonacci("5") is None


def test_fibonacci_float():
    assert fibonacci(5.0) is None


def test_fibonacci_boolean():
    assert fibonacci(True) is None


# ============================================================
# sum_of_digits
# ============================================================

def test_sum_of_digits():
    assert sum_of_digits(123) == 6


def test_sum_of_digits_single_digit():
    assert sum_of_digits(7) == 7


def test_sum_of_digits_zero():
    assert sum_of_digits(0) == 0


def test_sum_of_digits_large_number():
    assert sum_of_digits(123456789) == 45


def test_sum_of_digits_with_zero():
    assert sum_of_digits(1001) == 2


def test_sum_of_digits_negative():
    assert sum_of_digits(-123) == 6


def test_sum_of_digits_string():
    assert sum_of_digits("123") is None


def test_sum_of_digits_float():
    assert sum_of_digits(123.0) is None


def test_sum_of_digits_boolean():
    assert sum_of_digits(True) is None


def test_sum_of_digits_none():
    assert sum_of_digits(None) is None
