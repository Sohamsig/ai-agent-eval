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

    assert result == {
        "host": "localhost",
        "port": 8080,
        "timeout": 30,
    }


def test_invalid_config():
    assert create_client("invalid") is None


def test_invalid_port():
    assert create_client({
        "host": "localhost",
        "port": 70000,
    }) is None


def test_negative_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": -5,
    }) is None


def test_zero_timeout_is_valid():
    result = create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": 0,
    })

    assert result == {
        "host": "localhost",
        "port": 8080,
        "timeout": 0,
    }


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


def test_none_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": None,
    }) is None


def test_float_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": 10.5,
    }) is None


def test_valid_large_timeout():
    result = create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": 999999,
    })

    assert result == {
        "host": "localhost",
        "port": 8080,
        "timeout": 999999,
    }


def test_empty_host_rejected():
    assert create_client({
        "host": "",
        "port": 8080,
        "timeout": 10,
    }) is None


def test_invalid_host_type_rejected():
    assert create_client({
        "host": 123,
        "port": 8080,
        "timeout": 10,
    }) is None


def test_boolean_port_rejected():
    assert create_client({
        "host": "localhost",
        "port": True,
        "timeout": 10,
    }) is None


def test_zero_port_rejected():
    assert create_client({
        "host": "localhost",
        "port": 0,
        "timeout": 10,
    }) is None


def test_negative_port_rejected():
    assert create_client({
        "host": "localhost",
        "port": -1,
        "timeout": 10,
    }) is None


def test_maximum_valid_port():
    result = create_client({
        "host": "localhost",
        "port": 65535,
        "timeout": 10,
    })

    assert result == {
        "host": "localhost",
        "port": 65535,
        "timeout": 10,
    }