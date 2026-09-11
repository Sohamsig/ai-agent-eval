from url_utils import parse_url, build_url, add_query_params


def test_parse_url():
    result = parse_url(
        "https://example.com:8080/api/users?page=2#top"
    )

    assert result["scheme"] == "https"
    assert result["host"] == "example.com"
    assert result["port"] == 8080
    assert result["path"] == "/api/users"
    assert result["query"] == "page=2"
    assert result["fragment"] == "top"


def test_parse_url_without_port():
    result = parse_url("http://example.com/test")

    assert result["scheme"] == "http"
    assert result["host"] == "example.com"
    assert result["port"] is None
    assert result["path"] == "/test"


def test_build_url():
    result = build_url(
        "https",
        "example.com",
        "/search",
        {"q": "python", "page": 2}
    )

    assert result == "https://example.com/search?q=python&page=2"


def test_build_url_with_fragment():
    result = build_url(
        "https",
        "example.com",
        "/docs",
        {"page": 1},
        "top"
    )

    assert result == "https://example.com/docs?page=1#top"


def test_add_query_params():
    result = add_query_params(
        "https://example.com/search?q=python",
        {"page": 2}
    )

    assert result == "https://example.com/search?q=python&page=2"


def test_add_query_params_replaces_existing():
    result = add_query_params(
        "https://example.com/search?q=python&page=1",
        {"page": 2}
    )

    assert result == "https://example.com/search?q=python&page=2"
