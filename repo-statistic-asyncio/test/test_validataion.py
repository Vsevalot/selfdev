import pytest

from app.validation import (
    validate_url,
    validate_top_n,
    validate_days_to_old,
)
from app.exceptions import ArgumentException

@pytest.mark.parametrize('url', [
    'https://github.com/OWNER/REPOSITORY',
    'https://github.com/OWNER123/REPOSITORY',
    'https://github.com/OWNER/REPOSITORY123',
    'https://github.com/Vsevalot/AndHisNameIs/tree/main/app',
])
def test_validate_url(url):
    assert validate_url(url) is None

@pytest.mark.parametrize('url', [
    'https://github.com/REPOSITORY',
    'https://github.com/OWNER',
    'https://notagithub.com/OWNER/REPOSITORY',
    'asdasdsadsadasdasd',

])
def test_validate_url_fail(url):
    with pytest.raises(ArgumentException):
        validate_url(url)


def test_validate_top_n():
    assert validate_top_n(10) is None
    assert validate_top_n(100) is None
    assert validate_top_n(1000) is None

    with pytest.raises(ArgumentException):
        validate_top_n(0)
        validate_top_n(-10)


def test_validate_days_to_old():
    assert validate_days_to_old(10) is None
    assert validate_days_to_old(100) is None
    assert validate_days_to_old(1000) is None

    with pytest.raises(ArgumentException):
        validate_days_to_old(0)
        validate_days_to_old(-10)
