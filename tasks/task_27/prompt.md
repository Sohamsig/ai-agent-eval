# Task 27 — Refactor User Data Utilities

Refactor `actual_task_file.py`.

The current implementation contains duplicated validation and
normalization logic.

Your goal is to improve the internal structure and readability
without changing the public behavior.

## Requirements

1. Keep these public functions:

- `get_user_name`
- `get_user_email`
- `get_user_age`
- `format_user`
- `filter_users`

2. Remove unnecessary duplicated logic where practical.

3. You may introduce private helper functions.

4. Do not change the expected behavior.

5. Do not modify the tests.

6. Do not modify the public function signatures.

7. Do not mutate the input user dictionaries.

8. All tests must pass after the refactoring.

The objective is not to add new functionality.

The objective is to improve the internal code structure while
preserving existing behavior.
