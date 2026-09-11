from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def parse_url(url):
    parsed = urlparse(url)

    return {
        "scheme": parsed.scheme,
        "host": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment,
    }


def build_url(scheme, host, path, params=None, fragment=None):
    query = urlencode(params or {})

    return urlunparse((
        scheme,
        host,
        path,
        "",
        query,
        fragment or "",
    ))


def add_query_params(url, params):
    parsed = urlparse(url)
    existing = parse_qs(parsed.query)

    for key, value in params.items():
        existing[key] = [str(value)]

    query = urlencode(existing, doseq=True)

    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        query,
        parsed.fragment,
    ))