def calculate_total(items):
    total = 0

    for item in items:
        total += item["price"]

    return total


def apply_discount(total, discount_percent):
    if discount_percent < 0 or discount_percent > 100:
        return total

    return total - (total * discount_percent / 100)
