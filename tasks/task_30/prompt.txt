# Issue: Add order validation

## Problem

The order API currently assumes that every item is valid.

For example, the following input can cause errors:

- items that are not dictionaries
- items without a price
- items without a quantity
- negative prices
- zero or negative quantities
- boolean values used as prices or quantities

## Requested change

Improve `create_order()` so invalid orders are handled safely.

### Requirements

1. Validate that `items` is a list.
2. Every item must be a dictionary.
3. Every item must contain:
   - `name`
   - `price`
   - `quantity`
4. Price must be a non-negative number.
5. Quantity must be a positive integer.
6. Boolean values must not be accepted as price or quantity.
7. Invalid orders should return `None`.
8. Valid orders must continue to work exactly as before.
9. Do not break discount functionality.
10. Add meaningful tests for the new validation behavior.
11. Do not remove the existing tests.
12. Run the complete test suite after making the changes.

## Engineering expectation

Do not blindly modify the tests to make them pass.

First investigate how `create_order()`, `calculate_total()`, and
`apply_discount()` currently work.

Then implement the validation in an appropriate location while
keeping the existing functionality intact.
