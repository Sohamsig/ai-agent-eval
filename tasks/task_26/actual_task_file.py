"""
Task 26 - Price Calculation Utilities
"""


def calculate_subtotal(items):
    """Calculate the subtotal of an order."""
    total = 0

    for item in items:
        total += item["price"] * item["quantity"]

    return total


def apply_discount(amount, discount_percent):
    """Apply a percentage discount to an amount."""

    if discount_percent < 0 or discount_percent > 100:
        return amount

    discount = amount * discount_percent / 100

    return amount - discount


def calculate_tax(amount, tax_percent):
    """Calculate tax on an amount."""

    if amount < 0:
        return 0

    return round(amount + (amount * tax_percent / 100), 3)


def calculate_final_price(items, discount_percent=0, tax_percent=0):
    """Calculate final order price."""

    subtotal = calculate_subtotal(items)

    discounted = apply_discount(
        subtotal,
        discount_percent
    )

    final_price = calculate_tax(
        discounted,
        tax_percent
    )

    return round(final_price, 2)


def validate_items(items):
    """Validate order items."""

    if not isinstance(items, list) or not items:
        return False

    for item in items:
        if not isinstance(item, dict):
            return False

        if "price" not in item or "quantity" not in item:
            return False

        price = item["price"]
        quantity = item["quantity"]

        if not isinstance(price, (int, float)) or isinstance(price, bool):
            return False

        if price < 0:
            return False

        if not isinstance(quantity, int) or isinstance(quantity, bool):
            return False

        if quantity <= 0:
            return False

    return True
