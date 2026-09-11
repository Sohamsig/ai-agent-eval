import time


def _validate(operation, max_retries, delay):
    if not callable(operation):
        raise TypeError("operation must be callable")

    if not isinstance(max_retries, int) or isinstance(max_retries, bool):
        raise TypeError("max_retries must be an integer")

    if max_retries < 0:
        raise ValueError("max_retries cannot be negative")

    if not isinstance(delay, (int, float)) or isinstance(delay, bool):
        raise TypeError("delay must be a number")

    if delay < 0:
        raise ValueError("delay cannot be negative")


def retry(operation, max_retries=3, delay=0):
    """
    Execute an operation and retry it when it raises an exception.

    max_retries represents the number of retries after the
    initial attempt.

    Example:
        max_retries=3
        -> maximum of 4 total attempts.
    """

    _validate(operation, max_retries, delay)

    attempts = 0
    total_attempts = max_retries + 1

    while attempts < total_attempts:
        try:
            return operation()

        except Exception:
            attempts += 1

            if attempts >= total_attempts:
                raise

            if delay > 0:
                time.sleep(delay)


def retry_with_backoff(operation, max_retries=3, base_delay=1):
    """
    Execute an operation with exponential backoff.

    Delays between retries are:

        base_delay
        base_delay * 2
        base_delay * 4
        ...

    max_retries represents the number of retries after
    the initial attempt.
    """

    if not callable(operation):
        raise TypeError("operation must be callable")

    if not isinstance(max_retries, int) or isinstance(max_retries, bool):
        raise TypeError("max_retries must be an integer")

    if max_retries < 0:
        raise ValueError("max_retries cannot be negative")

    if not isinstance(base_delay, (int, float)) or isinstance(
        base_delay, bool
    ):
        raise TypeError("base_delay must be a number")

    if base_delay < 0:
        raise ValueError("base_delay cannot be negative")

    attempts = 0
    total_attempts = max_retries + 1

    while attempts < total_attempts:
        try:
            return operation()

        except Exception:
            attempts += 1

            if attempts >= total_attempts:
                raise

            delay = base_delay * (2 ** (attempts - 1))

            if delay > 0:
                time.sleep(delay)