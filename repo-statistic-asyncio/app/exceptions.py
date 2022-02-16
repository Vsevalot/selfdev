from requests import HTTPError, Response
from datetime import datetime
from aiohttp import ClientResponse, ClientError
from typing import Union


class ArgumentException(Exception):
    def __init__(self, argument: str):
        self.argument = argument


class DateArgumentException(ArgumentException):
    def __str__(self) -> str:
        return f"Can't parse argument {self.argument} to datetime." \
               f"Make sure the date is correct and " \
               f"use one of following formats: " \
               f"DD.MM.YY | DD.MM.YYYY | YYYY-MM-DD"


class RepoNotFoundException(Exception):
    def __init__(self, url: str):
        self.url = url

    def __str__(self):
        return f"Can't find given repository: {self.url}." \
               f" Please check the url and access to the repository."


class SomethingGoesWrongException(Exception):
    def __init__(self, exception: Exception):
        self.exception = exception

    def __str__(self) -> str:
        return f"Something goes wrong. Exception: {self.exception}"


class RateLimitException(Exception):
    def __init__(self, response: Response):
        self.max_requests = response.headers.get('X-RateLimit-Limit')
        self.reset_at = response.headers.get('X-RateLimit-Reset')
        self.reset_at = datetime.fromtimestamp(int(self.reset_at))
        self.is_authenticated = False
        if response.headers.get('github-authentication-token-expiration'):
            self.is_authenticated = True

    def __str__(self) -> str:
        res = f"Rate limit reached. " \
              f"You have {self.max_requests} requests per hour, " \
              f"rate limit resets at: {self.reset_at}."
        if not self.is_authenticated:
            res += " You can increase the rate limit " \
                   "by providing github token."
        return res


class TokenException(Exception):
    def __str__(self) -> str:
        return f"Bad credentials. Please check your token."


def _is_repo_not_found(response: Union[Response, ClientResponse]):
    if isinstance(response, Response):
        return response.status_code == 404
    elif isinstance(response, ClientResponse):
        return response.status == 404
    raise Exception("Unknown response type")


def _is_token_exception(response: Union[Response, ClientResponse]):
    if isinstance(response, Response):
        return response.status_code == 401
    elif isinstance(response, ClientResponse):
        return response.status == 401
    raise Exception("Unknown response type")


def raise_for_all(response: Union[Response, ClientResponse]):
    """
    Raises exceptions for all know errors or regular HTTPError if any found
    """
    if _is_repo_not_found(response):
        raise RepoNotFoundException(str(response.url))
    if _is_token_exception(response):
        raise TokenException()
    if response.headers.get('X-RateLimit-Remaining') == '0':
        raise RateLimitException(response)
    try:
        response.raise_for_status()
    except (HTTPError, ClientError) as e:
        raise SomethingGoesWrongException(e)


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
                ArgumentException,
                DateArgumentException,
                RepoNotFoundException,
                SomethingGoesWrongException,
                RateLimitException,
                TokenException,
        ) as e:
            print(e)
    return wrapper


def exception_handler_async(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (
                ArgumentException,
                DateArgumentException,
                RepoNotFoundException,
                SomethingGoesWrongException,
                RateLimitException,
                TokenException,
        ) as e:
            print(e)
    return wrapper
