from actual_task_file import create_order


def test_create_order_single_item():
    items = [
        {"name": "Book", "price": 100, "quantity": 1}
    ]

    result = create_order(items)

    assert result["total"] == 100


def test_create_order_multiple_items():
    items = [
        {"name": "Book", "price": 100, "quantity": 2},
        {"name": "Pen", "price": 20, "quantity": 3},
    ]

    result = create_order(items)

    assert result["total"] == 260


def test_create_order_discount():
    items = [
        {"name": "Book", "price": 100, "quantity": 2}
    ]

    result = create_order(items, 10)

    assert result["total"] == 180


def test_invalid_items_type():
    assert create_order("invalid") is None
