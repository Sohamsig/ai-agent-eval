from helpers import parse_config, get_timeout


def create_client(config):
    parsed = parse_config(config)

    if parsed is None:
        return None

    timeout = get_timeout(parsed)

    return {
        "host": parsed["host"],
        "port": parsed["port"],
        "timeout": timeout,
    }
