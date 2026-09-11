import csv
from io import StringIO


def parse_csv(text):
    """
    Parse CSV text into a list of dictionaries.

    The first row is treated as the header.
    """
    reader = csv.DictReader(StringIO(text))
    return list(reader)


def filter_rows(rows, column, value):
    """
    Return rows where the specified column equals value.
    """
    return [row for row in rows if row.get(column) == value]


def csv_to_text(rows, fieldnames):
    """
    Convert a list of dictionaries into CSV text.

    The first row contains the field names.
    """
    output = StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
        lineterminator="\n",
    )

    writer.writeheader()
    writer.writerows(rows)

    return output.getvalue()