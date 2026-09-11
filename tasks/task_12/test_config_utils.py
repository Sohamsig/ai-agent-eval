from config_utils import (
    get_config,
    set_config,
    merge_configs,
    remove_config,
)


def test_get_config():
    config = {"host": "localhost", "port": 8080}

    assert get_config(config, "host") == "localhost"


def test_get_config_default():
    config = {"host": "localhost"}

    assert get_config(config, "port", 3000) == 3000


def test_set_config():
    config = {"host": "localhost"}

    result = set_config(config, "port", 8080)

    assert result == {
        "host": "localhost",
        "port": 8080,
    }


def test_merge_configs():
    base = {
        "host": "localhost",
        "port": 8080,
    }

    override = {
        "port": 9000,
        "debug": True,
    }

    result = merge_configs(base, override)

    assert result == {
        "host": "localhost",
        "port": 9000,
        "debug": True,
    }


def test_merge_does_not_modify_original():
    base = {"host": "localhost"}
    override = {"port": 8080}

    result = merge_configs(base, override)

    assert base == {"host": "localhost"}
    assert override == {"port": 8080}
    assert result == {
        "host": "localhost",
        "port": 8080,
    }


def test_remove_config():
    config = {
        "host": "localhost",
        "port": 8080,
    }

    result = remove_config(config, "port")

    assert result == {
        "host": "localhost",
    }


def test_remove_missing_config():
    config = {"host": "localhost"}

    result = remove_config(config, "port")

    assert result == {
        "host": "localhost",
    }