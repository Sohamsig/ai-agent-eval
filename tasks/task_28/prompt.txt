# Task 28 — Improve Test Coverage

You are working on a Python number utility module.

The production implementation is in:

    actual_task_file.py

The existing tests are incomplete.

Your task is to inspect the implementation and improve the test
suite so that important normal cases, boundary cases, and invalid
inputs are covered.

## Public API

The following functions must be tested:

- `is_even`
- `is_prime`
- `factorial`
- `fibonacci`
- `sum_of_digits`

## Requirements

### is_even

Test:

- even positive numbers
- odd positive numbers
- zero
- negative numbers
- invalid input
- boolean input

### is_prime

Test:

- prime numbers
- non-prime numbers
- 0
- 1
- 2
- negative numbers
- even composite numbers
- odd composite numbers
- invalid input
- boolean input

### factorial

Test:

- 0
- 1
- normal positive values
- larger values
- negative values
- invalid input
- boolean input

### fibonacci

Test:

- 0
- 1
- several normal values
- larger values
- negative values
- invalid input
- boolean input

### sum_of_digits

Test:

- single digit
- multiple digits
- zero
- negative numbers
- numbers containing zero digits
- invalid input
- boolean input

## Important

Do not modify `actual_task_file.py`.

Your task is to improve the test suite.

Do not remove the existing tests.

Add meaningful tests rather than duplicate tests.

The tests should verify actual behavior and important edge cases.

Run the complete test suite after making your changes.
