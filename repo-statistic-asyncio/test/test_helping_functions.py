from datetime import datetime
import pytest

from app.helping_functions import (
    get_argument_date,
    parse_url,
)
from app.exceptions import DateArgumentException

date1 = datetime(day=10, month=11, year=2012)


@pytest.mark.parametrize("arg, expected", (
    ("10.11.12", date1),
    ("10.11.2012", date1),
    ("2012-11-10", date1),
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

@pytest.mark.parametrize("url", (
    'https://github.com/owner/repo',
    'https://github.com/owner/repo/tree/some_branch',
))
def test_parse_url(url):
    assert ('owner', 'repo') == parse_url(url)
