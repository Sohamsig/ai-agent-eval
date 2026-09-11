"""
Task 28 - Number Utilities

The implementation is intentionally kept simple.
The task is to improve the test coverage and verify
edge cases without changing the public API.
"""


def is_even(number):
    """Return True if number is even."""
    if not isinstance(number, int) or isinstance(number, bool):
        return False

    return number % 2 == 0


def is_prime(number):
    """Return True if number is a prime number."""
    if not isinstance(number, int) or isinstance(number, bool):
        return False

    if number < 2:
        return False

    if number == 2:
        return True

    if number % 2 == 0:
        return False

    divisor = 3

    while divisor * divisor <= number:
        if number % divisor == 0:
            return False

        divisor += 2

    return True


def factorial(number):
    """Return the factorial of a non-negative integer."""
    if not isinstance(number, int) or isinstance(number, bool):
        return None

    if number < 0:
        return None

    result = 1

    for value in range(2, number + 1):
        result *= value

    return result


def fibonacci(number):
    """Return the nth Fibonacci number."""
    if not isinstance(number, int) or isinstance(number, bool):
        return None

    if number < 0:
        return None

    if number == 0:
        return 0

    if number == 1:
        return 1

    previous = 0
    current = 1

    for _ in range(2, number + 1):
        previous, current = current, previous + current

    return current


def sum_of_digits(number):
    """Return the sum of the digits of an integer."""
    if not isinstance(number, int) or isinstance(number, bool):
        return None

    number = abs(number)

    total = 0

    while number > 0:
        total += number % 10
        number //= 10

    return total
