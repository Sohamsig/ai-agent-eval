from actual_task_file import create_client


def test_create_client():
    result = create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": 10,
    })

    assert result == {
        "host": "localhost",
        "port": 8080,
        "timeout": 10,
    }


def test_default_timeout():
    result = create_client({
        "host": "localhost",
        "port": 8080,
    })

    assert result["timeout"] == 30


def test_invalid_config():
    assert create_client("invalid") is None


def test_invalid_port():
    assert create_client({
        "host": "localhost",
        "port": 70000,
    }) is None
