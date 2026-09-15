from evaluator.failure_classifier import classify_failure


def test_success():
    result = classify_failure(
        return_code=0,
        stdout="5 passed",
    )

    assert result == "success"


def test_timeout():
    result = classify_failure(
        return_code=1,
        timed_out=True,
    )

    assert result == "timeout"


def test_assertion_error():
    result = classify_failure(
        return_code=1,
        stdout="AssertionError: expected 5 but got 4",
    )

    assert result == "assertion_error"


def test_import_error():
    result = classify_failure(
        return_code=1,
        stderr="ModuleNotFoundError: No module named 'example'",
    )

    assert result == "module_not_found"


def test_syntax_error():
    result = classify_failure(
        return_code=1,
        stderr="SyntaxError: invalid syntax",
    )

    assert result == "syntax_error"