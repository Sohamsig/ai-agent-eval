from sql_utils import (
    build_select_query,
    build_insert_query,
    build_update_query,
    build_delete_query,
)


def test_select_all():
    assert build_select_query("users") == "SELECT * FROM users"


def test_select_specific_columns():
    assert (
        build_select_query("users", ["id", "name"])
        == "SELECT id, name FROM users"
    )


def test_select_with_where():
    assert (
        build_select_query("users", ["id", "name"], {"id": 10})
        == "SELECT id, name FROM users WHERE id = $1"
    )


def test_select_multiple_conditions():
    assert (
        build_select_query(
            "users",
            ["id", "name"],
            {"id": 10, "active": True},
        )
        == "SELECT id, name FROM users WHERE id = $1 AND active = $2"
    )


def test_insert():
    assert (
        build_insert_query(
            "users",
            {"name": "Soham", "age": 20},
        )
        == "INSERT INTO users (name, age) VALUES ($1, $2)"
    )


def test_update():
    assert (
        build_update_query(
            "users",
            {"name": "John", "age": 25},
            {"id": 1},
        )
        == "UPDATE users SET name = $1, age = $2 WHERE id = $3"
    )


def test_update_multiple_conditions():
    assert (
        build_update_query(
            "users",
            {"active": True},
            {"id": 1, "role": "admin"},
        )
        == "UPDATE users SET active = $1 WHERE id = $2 AND role = $3"
    )


def test_delete():
    assert (
        build_delete_query(
            "users",
            {"id": 1},
        )
        == "DELETE FROM users WHERE id = $1"
    )


def test_invalid_table():
    assert build_select_query("users; DROP TABLE users") is None


def test_invalid_column():
    assert build_select_query("users", ["id", "name; DROP TABLE users"]) is None


def test_empty_columns():
    assert build_select_query("users", []) is None


def test_invalid_data():
    assert build_insert_query("users", {}) is None


def test_invalid_where():
    assert build_delete_query("users", {}) is None


def test_invalid_update_data():
    assert build_update_query("users", {}, {"id": 1}) is None


def test_invalid_update_where():
    assert build_update_query("users", {"name": "x"}, {}) is None