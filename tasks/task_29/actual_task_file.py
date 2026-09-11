from helpers import calculate_total, apply_discount


def create_order(items, discount_percent=0):
    if not isinstance(items, list):
        return None

    total = calculate_total(items)
    total = apply_discount(total, discount_percent)

    return {
        "items": items,
        "total": round(total, 2),
    }
