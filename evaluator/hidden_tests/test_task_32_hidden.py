from actual_task_file import create_client


def test_negative_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": -5,
    }) is None


def test_string_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": "10",
    }) is None


def test_boolean_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": True,
    }) is None


def test_zero_timeout_is_valid():
    result = create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": 0,
    })

    assert result["timeout"] == 0


def test_none_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": None,
    }) is None


def test_missing_timeout_uses_default():
    result = create_client({
        "host": "localhost",
        "port": 8080,
    })

    assert result["timeout"] == 30
