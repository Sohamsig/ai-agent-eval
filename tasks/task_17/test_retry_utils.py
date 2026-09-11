import pytest

from retry_utils import retry, retry_with_backoff


def test_retry_success_first_attempt():
    calls = []

    def operation():
        calls.append(1)
        return "success"

    result = retry(operation, max_retries=3)

    assert result == "success"
    assert len(calls) == 1


def test_retry_success_after_failures():
    calls = []

    def operation():
        calls.append(1)

        if len(calls) < 3:
            raise ValueError("temporary failure")

        return "success"

    result = retry(operation, max_retries=3, delay=0)

    assert result == "success"
    assert len(calls) == 3


def test_retry_exhausted():
    calls = []

    def operation():
        calls.append(1)
        raise ValueError("failure")

    with pytest.raises(ValueError, match="failure"):
        retry(operation, max_retries=3, delay=0)

    assert len(calls) == 4


def test_retry_zero_retries():
    calls = []

    def operation():
        calls.append(1)
        raise RuntimeError("failed")

    with pytest.raises(RuntimeError):
        retry(operation, max_retries=0, delay=0)

    assert len(calls) == 1


def test_retry_negative_retries():
    calls = []

    def operation():
        calls.append(1)
        return "success"

    with pytest.raises(ValueError):
        retry(operation, max_retries=-1, delay=0)

    assert len(calls) == 0


def test_retry_invalid_operation():
    with pytest.raises(TypeError):
        retry(None, max_retries=2, delay=0)


def test_retry_invalid_max_retries():
    def operation():
        return "success"

    with pytest.raises(ValueError):
        retry(operation, max_retries=-1, delay=0)


def test_retry_invalid_delay():
    def operation():
        return "success"

    with pytest.raises(ValueError):
        retry(operation, max_retries=2, delay=-1)


def test_retry_with_backoff_success():
    calls = []

    def operation():
        calls.append(1)

        if len(calls) < 3:
            raise ValueError("temporary failure")

        return "success"

    result = retry_with_backoff(
        operation,
        max_retries=3,
        base_delay=0,
    )

    assert result == "success"
    assert len(calls) == 3


def test_retry_with_backoff_exhausted():
    calls = []

    def operation():
        calls.append(1)
        raise RuntimeError("permanent failure")

    with pytest.raises(RuntimeError, match="permanent failure"):
        retry_with_backoff(
            operation,
            max_retries=2,
            base_delay=0,
        )

    assert len(calls) == 3


def test_retry_with_backoff_zero_retries():
    calls = []

    def operation():
        calls.append(1)
        raise RuntimeError("failed")

    with pytest.raises(RuntimeError):
        retry_with_backoff(
            operation,
            max_retries=0,
            base_delay=0,
        )

    assert len(calls) == 1


def test_retry_with_backoff_invalid_base_delay():
    def operation():
        return "success"

    with pytest.raises(ValueError):
        retry_with_backoff(
            operation,
            max_retries=2,
            base_delay=-1,
        )


def test_retry_with_backoff_invalid_operation():
    with pytest.raises(TypeError):
        retry_with_backoff(
            None,
            max_retries=2,
            base_delay=0,
        )