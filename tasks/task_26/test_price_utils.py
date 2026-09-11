import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parent / "actual_task_file.py"

spec = importlib.util.spec_from_file_location(
    "actual_task_file",
    MODULE_PATH
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


calculate_subtotal = module.calculate_subtotal
apply_discount = module.apply_discount
calculate_tax = module.calculate_tax
calculate_final_price = module.calculate_final_price
validate_items = module.validate_items


# ============================================================
# calculate_subtotal
# ============================================================

def test_calculate_subtotal_single_item():
    items = [
        {"price": 100, "quantity": 2}
    ]

    assert calculate_subtotal(items) == 200


def test_calculate_subtotal_multiple_items():
    items = [
        {"price": 100, "quantity": 2},
        {"price": 50, "quantity": 3},
    ]

    assert calculate_subtotal(items) == 350


def test_calculate_subtotal_decimal_prices():
    items = [
        {"price": 10.50, "quantity": 2},
        {"price": 5.25, "quantity": 4},
    ]

    assert calculate_subtotal(items) == 42.0


def test_calculate_subtotal_empty_list():
    assert calculate_subtotal([]) == 0


def test_calculate_subtotal_quantity_one():
    items = [
        {"price": 75, "quantity": 1}
    ]

    assert calculate_subtotal(items) == 75


# ============================================================
# apply_discount
# ============================================================

def test_apply_discount_10_percent():
    assert apply_discount(100, 10) == 90


def test_apply_discount_20_percent():
    assert apply_discount(250, 20) == 200


def test_apply_discount_50_percent():
    assert apply_discount(1000, 50) == 500


def test_apply_discount_zero_percent():
    assert apply_discount(100, 0) == 100


def test_apply_discount_100_percent():
    assert apply_discount(100, 100) == 0


def test_apply_discount_invalid_negative_percent():
    assert apply_discount(100, -10) == 100


def test_apply_discount_invalid_over_100_percent():
    assert apply_discount(100, 120) == 100


def test_apply_discount_decimal_amount():
    assert apply_discount(99.99, 10) == 89.991


# ============================================================
# calculate_tax
# ============================================================

def test_calculate_tax_10_percent():
    assert calculate_tax(100, 10) == 110


def test_calculate_tax_18_percent():
    assert calculate_tax(100, 18) == 118


def test_calculate_tax_zero_percent():
    assert calculate_tax(100, 0) == 100


def test_calculate_tax_on_decimal_amount():
    assert calculate_tax(99.99, 10) == 109.989


def test_calculate_tax_negative_amount():
    assert calculate_tax(-100, 10) == 0


# ============================================================
# calculate_final_price
# ============================================================

def test_final_price_without_discount_or_tax():
    items = [
        {"price": 100, "quantity": 2}
    ]

    assert calculate_final_price(items) == 200


def test_final_price_with_discount():
    items = [
        {"price": 100, "quantity": 2}
    ]

    assert calculate_final_price(
        items,
        discount_percent=10
    ) == 180


def test_final_price_with_tax():
    items = [
        {"price": 100, "quantity": 2}
    ]

    assert calculate_final_price(
        items,
        tax_percent=10
    ) == 220


def test_final_price_with_discount_and_tax():
    items = [
        {"price": 100, "quantity": 2}
    ]

    assert calculate_final_price(
        items,
        discount_percent=10,
        tax_percent=10
    ) == 198


def test_final_price_multiple_items():
    items = [
        {"price": 100, "quantity": 2},
        {"price": 50, "quantity": 3},
    ]

    assert calculate_final_price(
        items,
        discount_percent=10,
        tax_percent=18
    ) == 371.7


def test_final_price_empty_order():
    assert calculate_final_price([]) == 0


def test_final_price_rounds_to_two_decimals():
    items = [
        {"price": 19.99, "quantity": 3}
    ]

    result = calculate_final_price(
        items,
        discount_percent=10,
        tax_percent=18
    )

    assert result == 63.69


# ============================================================
# validate_items
# ============================================================

def test_validate_items_valid_order():
    items = [
        {"price": 100, "quantity": 2}
    ]

    assert validate_items(items) is True


def test_validate_items_multiple_items():
    items = [
        {"price": 100, "quantity": 2},
        {"price": 50, "quantity": 1},
    ]

    assert validate_items(items) is True


def test_validate_items_empty_list():
    assert validate_items([]) is False


def test_validate_items_missing_price():
    items = [
        {"quantity": 2}
    ]

    assert validate_items(items) is False


def test_validate_items_missing_quantity():
    items = [
        {"price": 100}
    ]

    assert validate_items(items) is False


def test_validate_items_negative_price():
    items = [
        {"price": -100, "quantity": 2}
    ]

    assert validate_items(items) is False


def test_validate_items_zero_quantity():
    items = [
        {"price": 100, "quantity": 0}
    ]

    assert validate_items(items) is False


def test_validate_items_negative_quantity():
    items = [
        {"price": 100, "quantity": -2}
    ]

    assert validate_items(items) is False


def test_validate_items_non_numeric_price():
    items = [
        {"price": "100", "quantity": 2}
    ]

    assert validate_items(items) is False


def test_validate_items_non_integer_quantity():
    items = [
        {"price": 100, "quantity": 2.5}
    ]

    assert validate_items(items) is False
