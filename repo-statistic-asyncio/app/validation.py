from argparse import Namespace
from typing import NoReturn

from app.exceptions import ArgumentException
from app.helping_functions import get_argument_date, parse_url


def validate_url(url: str) -> NoReturn:
    try:
        owner, repo = parse_url(url)
    except ValueError:
        raise ArgumentException(f'Invalid GitHub repository URL: {url}')


def validate_date(date: str) -> NoReturn:
    get_argument_date(date)


def validate_top_n(top_n: int) -> NoReturn:
    if top_n < 1:
        raise ArgumentException(f'Top N contributors must be greater than 0, '
                                f'you set {top_n}')


def validate_days_to_old(days_to_old: int) -> NoReturn:
    if days_to_old < 0:
        raise ArgumentException(f'Days to old must be greater than 0, '
                                f'you set {days_to_old}')


def validate_args(args: Namespace) -> NoReturn:
    validate_url(args.url)
    if args.since:
        validate_date(args.since)
    if args.until:
        validate_date(args.until)
    validate_top_n(args.top_contributors)
    validate_days_to_old(args.days_to_old)
