from datetime import datetime
import pytest

from app.helping_functions import (
    get_argument_date,
    get_time_period_string,
)
from app.exceptions import DateArgumentException

ex1 = datetime(day=10, month=11, year=2012)
ex2 = datetime(day=3, month=5, year=2017)


@pytest.mark.parametrize("arg, expected", (
    ("10.11.12", ex1),
    ("10.11.2012", ex1),
    ("2012-11-10", ex1),
))
def test_get_argument_date(arg, expected):
    assert expected == get_argument_date(arg)


@pytest.mark.parametrize("arg", (
    "asasadad",
    "33.01.2005",
    "14:12:13",
))
def test_get_argument_date_raises(arg):
    with pytest.raises(DateArgumentException):
        get_argument_date("asdasdas")


@pytest.mark.parametrize("arg1, arg2, expected", (
    (ex1, ex2, f"from {ex1} to {ex2}"),
    (ex1, None, f"from {ex1} to now"),
    (None, ex2, f"from the beginning to {ex2}"),
    (None, None, "for the all time"),
))
def test_get_time_period_string(arg1, arg2, expected):
    assert expected == get_time_period_string(
        since=arg1,
        until=arg2,
    )
