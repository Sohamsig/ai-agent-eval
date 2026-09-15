import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluator.evaluate import classify_test_failure


def test_success():
    assert classify_test_failure(
        stdout="11 passed",
        stderr="",
        return_code=0,
    ) == "success"


def test_syntax_error():
    assert classify_test_failure(
        stdout="",
        stderr="SyntaxError: invalid syntax",
        return_code=1,
    ) == "syntax_error"


def test_import_error():
    assert classify_test_failure(
        stdout="",
        stderr="ModuleNotFoundError: No module named 'cache_utils'",
        return_code=1,
    ) == "import_error"


def test_type_error():
    assert classify_test_failure(
        stdout="",
        stderr="TypeError: invalid argument",
        return_code=1,
    ) == "type_error"


def test_name_error():
    assert classify_test_failure(
        stdout="",
        stderr="NameError: name 'x' is not defined",
        return_code=1,
    ) == "name_error"


def test_attribute_error():
    assert classify_test_failure(
        stdout="",
        stderr="AttributeError: object has no attribute 'x'",
        return_code=1,
    ) == "attribute_error"


def test_key_error():
    assert classify_test_failure(
        stdout="",
        stderr="KeyError: 'missing'",
        return_code=1,
    ) == "key_error"


def test_index_error():
    assert classify_test_failure(
        stdout="",
        stderr="IndexError: list index out of range",
        return_code=1,
    ) == "index_error"


def test_assertion_failure():
    assert classify_test_failure(
        stdout="FAILED test_cache.py::test_get",
        stderr="AssertionError: expected 1 but got 2",
        return_code=1,
    ) == "assertion_failure"


def test_timeout():
    assert classify_test_failure(
        stdout="",
        stderr="Test execution timed out after 120 seconds",
        return_code=1,
    ) == "timeout"


def test_connection_error():
    assert classify_test_failure(
        stdout="",
        stderr="ConnectionError: connection refused",
        return_code=1,
    ) == "connection_error"


def test_permission_error():
    assert classify_test_failure(
        stdout="",
        stderr="PermissionError: permission denied",
        return_code=1,
    ) == "permission_error"


def test_evaluator_error():
    assert classify_test_failure(
        stdout="",
        stderr="pytest internal error",
        return_code=1,
    ) == "evaluator_error"


def test_generic_test_failure():
    assert classify_test_failure(
        stdout="Some test failed",
        stderr="Unexpected behavior",
        return_code=1,
    ) == "assertion_failure"