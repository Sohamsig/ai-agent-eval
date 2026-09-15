from helpers import parse_config, get_timeout


def create_client(config):
    """
    Create a client configuration.

    Returns:
        dict: Valid client configuration.
        None: If the configuration is invalid.
    """

    parsed = parse_config(config)

    if parsed is None:
        return None

    timeout = get_timeout(parsed)

    return {
        "host": parsed["host"],
        "port": parsed["port"],
        "timeout": timeout,
    }