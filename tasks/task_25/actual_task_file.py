from datetime import date, timedelta


def parse_date(value):
    """Parse YYYY-MM-DD into a date object."""

    if not isinstance(value, str) or not value:
        raise ValueError("Invalid date")

    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Invalid date") from exc


def format_date(value):
    """Format date as YYYY-MM-DD."""

    if not isinstance(value, date):
        raise ValueError("Expected a date object")

    return value.strftime("%Y-%m-%d")


def days_between(start, end):
    """Return absolute number of days between two dates."""

    return abs((end - start).days)


def is_leap_year(year):
    """Check whether a year is a Gregorian leap year."""

    return year % 4 == 0 and (
        year % 100 != 0 or year % 400 == 0
    )


def add_days(value, days):
    """Add days to a date."""

    return value + timedelta(days=days)


def get_month_name(value):
    """Return full month name."""

    return value.strftime("%B")


def get_weekday_name(value):
    """Return full weekday name."""

    return value.strftime("%A")