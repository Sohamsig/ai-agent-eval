def parse_config(config):
    if not isinstance(config, dict):
        return None

    host = config.get("host")
    port = config.get("port")

    if not isinstance(host, str) or not host:
        return None

    if not isinstance(port, int) or isinstance(port, bool):
        return None

    if port <= 0 or port > 65535:
        return None

    return {
        "host": host,
        "port": port,
        "timeout": config.get("timeout", 30),
    }


def get_timeout(config):
    timeout = config.get("timeout", 30)

    if timeout < 0:
        return 30

    return timeout
