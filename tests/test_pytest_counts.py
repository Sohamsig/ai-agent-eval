from evaluator.evaluate import parse_pytest_counts


def test_parse_all_passed():
    result = parse_pytest_counts(
        "================ 17 passed in 0.09s ================"
    )

    assert result["tests_total"] == 17
    assert result["tests_passed_count"] == 17
    assert result["tests_failed_count"] == 0
    assert result["tests_skipped_count"] == 0


def test_parse_failed_and_passed():
    result = parse_pytest_counts(
        "================ 4 failed, 13 passed in 0.09s ================"
    )

    assert result["tests_total"] == 17
    assert result["tests_passed_count"] == 13
    assert result["tests_failed_count"] == 4
    assert result["tests_skipped_count"] == 0


def test_parse_failed_passed_and_skipped():
    result = parse_pytest_counts(
        "================ 1 failed, 14 passed, 2 skipped in 0.09s ================"
    )

    assert result["tests_total"] == 17
    assert result["tests_passed_count"] == 14
    assert result["tests_failed_count"] == 1
    assert result["tests_skipped_count"] == 2


def test_parse_empty_output():
    result = parse_pytest_counts("")

    assert result["tests_total"] is None
    assert result["tests_passed_count"] is None
    assert result["tests_failed_count"] is None
    assert result["tests_skipped_count"] is None


def test_parse_unrecognized_output():
    result = parse_pytest_counts("pytest encountered an unexpected error")

    assert result["tests_total"] is None
    assert result["tests_passed_count"] is None
    assert result["tests_failed_count"] is None
    assert result["tests_skipped_count"] is None
