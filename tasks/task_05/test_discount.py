from discount import calculate_discount


def test_calculate_discount():
    assert calculate_discount(100, 20) == 80


def test_no_discount():
    assert calculate_discount(100, 0) == 100


def test_fifty_percent_discount():
    assert calculate_discount(200, 50) == 100