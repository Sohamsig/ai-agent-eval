from datetime import date

import pytest

from tasks.task_25.actual_task_file import (
    parse_date,
    format_date,
    days_between,
    is_leap_year,
    add_days,
    get_month_name,
    get_weekday_name,
)


# ---------------------------------------------------------
# parse_date
# ---------------------------------------------------------

def test_parse_date():
    result = parse_date("2026-09-05")

    assert isinstance(result, date)
    assert result == date(2026, 9, 5)


def test_parse_date_new_year():
    assert parse_date("2025-01-01") == date(2025, 1, 1)


def test_parse_date_leap_day():
    assert parse_date("2024-02-29") == date(2024, 2, 29)


def test_parse_date_invalid_format():
    with pytest.raises(ValueError):
        parse_date("05-09-2026")


def test_parse_date_invalid_day():
    with pytest.raises(ValueError):
        parse_date("2026-09-31")


def test_parse_date_invalid_month():
    with pytest.raises(ValueError):
        parse_date("2026-13-01")


def test_parse_date_empty_string():
    with pytest.raises(ValueError):
        parse_date("")


# ---------------------------------------------------------
# format_date
# ---------------------------------------------------------

def test_format_date():
    result = format_date(date(2026, 9, 5))

    assert result == "2026-09-05"


def test_format_date_single_digit_month():
    assert format_date(date(2026, 2, 3)) == "2026-02-03"


def test_format_date_single_digit_day():
    assert format_date(date(2026, 10, 7)) == "2026-10-07"


# ---------------------------------------------------------
# days_between
# ---------------------------------------------------------

def test_days_between_forward():
    start = date(2026, 1, 1)
    end = date(2026, 1, 10)

    assert days_between(start, end) == 9


def test_days_between_reverse():
    start = date(2026, 1, 10)
    end = date(2026, 1, 1)

    assert days_between(start, end) == 9


def test_days_between_same_date():
    d = date(2026, 5, 15)

    assert days_between(d, d) == 0


def test_days_between_across_month():
    start = date(2026, 1, 30)
    end = date(2026, 2, 2)

    assert days_between(start, end) == 3


def test_days_between_across_year():
    start = date(2025, 12, 31)
    end = date(2026, 1, 2)

    assert days_between(start, end) == 2


# ---------------------------------------------------------
# is_leap_year
# ---------------------------------------------------------

def test_regular_leap_year():
    assert is_leap_year(2024) is True


def test_non_leap_year():
    assert is_leap_year(2025) is False


def test_century_non_leap_year():
    assert is_leap_year(1900) is False


def test_century_leap_year():
    assert is_leap_year(2000) is True


def test_2100_not_leap_year():
    assert is_leap_year(2100) is False


def test_2400_leap_year():
    assert is_leap_year(2400) is True


# ---------------------------------------------------------
# add_days
# ---------------------------------------------------------

def test_add_days():
    original = date(2026, 1, 1)

    result = add_days(original, 10)

    assert result == date(2026, 1, 11)


def test_add_zero_days():
    original = date(2026, 5, 10)

    result = add_days(original, 0)

    assert result == original


def test_add_negative_days():
    original = date(2026, 5, 10)

    result = add_days(original, -5)

    assert result == date(2026, 5, 5)


def test_add_days_across_month():
    original = date(2026, 1, 30)

    assert add_days(original, 3) == date(2026, 2, 2)


def test_add_days_across_year():
    original = date(2025, 12, 31)

    assert add_days(original, 1) == date(2026, 1, 1)


def test_add_days_does_not_modify_original():
    original = date(2026, 1, 1)

    add_days(original, 20)

    assert original == date(2026, 1, 1)


# ---------------------------------------------------------
# get_month_name
# ---------------------------------------------------------

def test_get_month_name_january():
    assert get_month_name(date(2026, 1, 15)) == "January"


def test_get_month_name_march():
    assert get_month_name(date(2026, 3, 10)) == "March"


def test_get_month_name_december():
    assert get_month_name(date(2026, 12, 25)) == "December"


def test_get_month_name_august():
    assert get_month_name(date(2026, 8, 20)) == "August"


# ---------------------------------------------------------
# get_weekday_name
# ---------------------------------------------------------

def test_get_weekday_name_monday():
    assert get_weekday_name(date(2026, 9, 7)) == "Monday"


def test_get_weekday_name_tuesday():
    assert get_weekday_name(date(2026, 9, 8)) == "Tuesday"


def test_get_weekday_name_sunday():
    assert get_weekday_name(date(2026, 9, 6)) == "Sunday"


def test_get_weekday_name_saturday():
    assert get_weekday_name(date(2026, 9, 5)) == "Saturday"