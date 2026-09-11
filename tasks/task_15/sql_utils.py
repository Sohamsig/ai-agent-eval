import re


_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _valid_identifier(value):
    return isinstance(value, str) and bool(_IDENTIFIER_RE.fullmatch(value))


def _build_conditions(where, start_index=1):
    if not isinstance(where, dict) or not where:
        return None

    conditions = []
    index = start_index

    for column in where:
        if not _valid_identifier(column):
            return None

        conditions.append(f"{column} = ${index}")
        index += 1

    return " AND ".join(conditions)


def build_select_query(table, columns=None, where=None):
    if not _valid_identifier(table):
        return None

    if columns is None:
        column_sql = "*"
    else:
        if not isinstance(columns, (list, tuple)) or not columns:
            return None

        if not all(_valid_identifier(column) for column in columns):
            return None

        column_sql = ", ".join(columns)

    query = f"SELECT {column_sql} FROM {table}"

    if where is not None:
        conditions = _build_conditions(where)

        if conditions is None:
            return None

        query += f" WHERE {conditions}"

    return query


def build_insert_query(table, data):
    if not _valid_identifier(table):
        return None

    if not isinstance(data, dict) or not data:
        return None

    columns = list(data.keys())

    if not all(_valid_identifier(column) for column in columns):
        return None

    placeholders = [
        f"${index}"
        for index in range(1, len(columns) + 1)
    ]

    return (
        f"INSERT INTO {table} "
        f"({', '.join(columns)}) "
        f"VALUES ({', '.join(placeholders)})"
    )


def build_update_query(table, data, where):
    if not _valid_identifier(table):
        return None

    if not isinstance(data, dict) or not data:
        return None

    if not isinstance(where, dict) or not where:
        return None

    columns = list(data.keys())

    if not all(_valid_identifier(column) for column in columns):
        return None

    set_parts = []

    for index, column in enumerate(columns, start=1):
        set_parts.append(f"{column} = ${index}")

    conditions = _build_conditions(
        where,
        start_index=len(columns) + 1
    )

    if conditions is None:
        return None

    return (
        f"UPDATE {table} "
        f"SET {', '.join(set_parts)} "
        f"WHERE {conditions}"
    )


def build_delete_query(table, where):
    if not _valid_identifier(table):
        return None

    if not isinstance(where, dict) or not where:
        return None

    conditions = _build_conditions(where)

    if conditions is None:
        return None

    return f"DELETE FROM {table} WHERE {conditions}"
