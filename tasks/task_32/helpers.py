def parse_config(config):
    """
    Validate and normalize the client configuration.

    Returns:
        dict: Validated configuration.
        None: If configuration is invalid.
    """

    if not isinstance(config, dict):
        return None

    host = config.get("host")
    port = config.get("port")

    # Host validation
    if not isinstance(host, str) or not host:
        return None

    # bool is a subclass of int, so explicitly reject bool.
    if not isinstance(port, int) or isinstance(port, bool):
        return None

    # Port range validation
    if port <= 0 or port > 65535:
        return None

    # Preserve the distinction between:
    # - missing timeout: use default 30
    # - timeout=None: invalid
    timeout = config.get("timeout", 30)

    # Timeout must be an integer.
    # Boolean values must not be accepted.
    if not isinstance(timeout, int) or isinstance(timeout, bool):
        return None

    # Timeout must be greater than or equal to zero.
    if timeout < 0:
        return None

    return {
        "host": host,
        "port": port,
        "timeout": timeout,
    }


def get_timeout(config):
    """
    Return the already-validated timeout.

    The configuration is expected to be validated by parse_config().
    """

    return config["timeout"]