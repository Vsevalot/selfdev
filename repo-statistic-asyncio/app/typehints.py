from typing import (
    TypedDict,
    Union,
)
from requests.models import CaseInsensitiveDict
from multidict import CIMultiDictProxy


HeadersType = Union[CaseInsensitiveDict, CIMultiDictProxy]


class AuthorType(TypedDict):
    login: str


class CommitType(TypedDict):
    author: AuthorType
