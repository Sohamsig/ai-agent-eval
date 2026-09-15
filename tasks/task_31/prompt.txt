# Task 31 — Implementation ? Tests

You are working on a small Python user-management repository.

The production implementation already exists in:

    actual_task_file.py

Your task is to improve the test suite.

## Requirements

1. Carefully inspect actual_task_file.py before writing tests.
2. Test all public functions:
   - normalize_email()
   - is_valid_email()
   - create_user()
3. Keep all existing tests.
4. Add meaningful tests for:
   - normal inputs
   - empty strings
   - whitespace
   - uppercase input
   - invalid email formats
   - missing email components
   - invalid data types
   - invalid user names
   - boundary cases
5. Test interactions between the functions through create_user().
6. Do not modify actual_task_file.py.
7. Do not remove or weaken existing tests.
8. Do not simply duplicate existing tests with different values.
9. Run the complete test suite after adding the tests.
10. Make sure the new tests actually verify observable behavior.

## Engineering expectation

The goal is not to maximize the raw number of tests.

The goal is to identify important behaviors and edge cases that are
currently insufficiently covered by the existing test suite.

Your changes should improve confidence in the existing implementation
without modifying production code.
