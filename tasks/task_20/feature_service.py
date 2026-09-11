from feature_utils import add_numbers, multiply_numbers


def calculate(a, b):
    """Return a dictionary containing sum and product."""
    total = add_numbers(a, b)
    product = multiply_numbers(a, b)

    if total is None or product is None:
        return None

    return {
        "sum": total,
        "product": product,
    }


def calculate_sum(a, b):
    """Return the sum using the utility module."""
    return add_numbers(a, b)


def calculate_product(a, b):
    """Return the product using the utility module."""
    return multiply_numbers(a, b)