from actual_task_file import create_order


def test_create_order_single_item():
    items = [{"name": "Book", "price": 100}]
    result = create_order(items)

    assert result["total"] == 100


def test_create_order_multiple_items():
    items = [
        {"name": "Book", "price": 100},
        {"name": "Pen", "price": 20},
    ]

    result = create_order(items)

    assert result["total"] == 120


def test_create_order_discount():
    items = [{"name": "Book", "price": 100}]

    result = create_order(items, 10)

    assert result["total"] == 90


def test_invalid_items():
    assert create_order("invalid") is None
