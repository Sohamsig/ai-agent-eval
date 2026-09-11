from csv_utils import parse_csv, filter_rows, csv_to_text


def test_parse_csv():
    text = "name,age\nAlice,25\nBob,30\n"

    result = parse_csv(text)

    assert result == [
        {"name": "Alice", "age": "25"},
        {"name": "Bob", "age": "30"},
    ]


def test_parse_csv_multiple_columns():
    text = "name,city,role\nAlice,Pune,Engineer\nBob,Mumbai,Designer\n"

    result = parse_csv(text)

    assert result[0]["name"] == "Alice"
    assert result[0]["city"] == "Pune"
    assert result[0]["role"] == "Engineer"


def test_filter_rows():
    rows = [
        {"name": "Alice", "city": "Pune"},
        {"name": "Bob", "city": "Mumbai"},
        {"name": "Charlie", "city": "Pune"},
    ]

    result = filter_rows(rows, "city", "Pune")

    assert result == [
        {"name": "Alice", "city": "Pune"},
        {"name": "Charlie", "city": "Pune"},
    ]


def test_filter_rows_no_match():
    rows = [
        {"name": "Alice", "city": "Pune"},
        {"name": "Bob", "city": "Mumbai"},
    ]

    result = filter_rows(rows, "city", "Delhi")

    assert result == []


def test_csv_to_text():
    rows = [
        {"name": "Alice", "age": "25"},
        {"name": "Bob", "age": "30"},
    ]

    result = csv_to_text(rows, ["name", "age"])

    assert result == (
        "name,age\n"
        "Alice,25\n"
        "Bob,30\n"
    )


def test_csv_to_text_with_special_characters():
    rows = [
        {"name": "Alice Smith", "city": "New York, NY"},
    ]

    result = csv_to_text(rows, ["name", "city"])

    assert result == (
        "name,city\n"
        "Alice Smith,\"New York, NY\"\n"
    )