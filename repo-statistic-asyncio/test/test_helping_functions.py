from datetime import datetime
import pytest

from app.helping_functions import (
    get_argument_date,
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
        get_argument_date(arg)
