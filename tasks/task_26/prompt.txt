# Task 26 — Fix Order Price Calculation

You are working on an existing Python codebase.

The file `actual_task_file.py` contains several bugs in an order
price calculation utility.

Your task is to investigate the implementation and fix all bugs.

## Requirements

### 1. calculate_subtotal(items)

Calculate:

    price × quantity

for every item and return the sum.

Example:

    [
        {"price": 100, "quantity": 2},
        {"price": 50, "quantity": 3}
    ]

should return:

    350

An empty list should return `0`.

---

### 2. apply_discount(amount, discount_percent)

Apply the percentage discount correctly.

For example:

    apply_discount(100, 10)

should return:

    90

Discount percentages below 0 or above 100 should leave the
original amount unchanged.

---

### 3. calculate_tax(amount, tax_percent)

Return the amount including tax.

For example:

    calculate_tax(100, 18)

should return:

    118

A negative amount should return `0`.

---

### 4. calculate_final_price(items, discount_percent, tax_percent)

The calculation order must be:

1. Calculate subtotal.
2. Apply discount.
3. Apply tax.
4. Round the final result to two decimal places.

---

### 5. validate_items(items)

An order is valid only when:

- `items` is not empty.
- Every item contains `price`.
- Every item contains `quantity`.
- `price` is numeric.
- `price` is not negative.
- `quantity` is an integer.
- `quantity` is greater than zero.

Return `True` for valid input and `False` otherwise.

## Important

Do not change the function names.

Do not remove functionality.

Do not modify the tests.

Fix the implementation so that the complete test suite passes.
