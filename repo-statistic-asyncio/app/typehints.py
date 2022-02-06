from typing import Union, Optional
from enum import Enum
from pydantic import BaseModel
from requests.models import CaseInsensitiveDict
from multidict import CIMultiDictProxy
from datetime import datetime


HeadersType = Union[CaseInsensitiveDict, CIMultiDictProxy]


class UserShort(BaseModel):
    name: str
    email: str


class Commit(BaseModel):
    url: str
    author: UserShort
    committer: UserShort
    message: str


class User(BaseModel):
    login: str


class CommitInfo(BaseModel):
    commit: Commit
    author: Optional[User]
    committer: Optional[User]

    def get_contributor(self) -> str:
        if self.author is None:
            return self.commit.author.name
        return self.author.login



class _EventState(str, Enum):
    open = "open"
    closed = "closed"


class EventInfo(BaseModel):
    url: str
    state: _EventState
    created_at: datetime
    closed_at: Optional[datetime]


class PRInfo(EventInfo):
    draft: bool


class IssueInfo(EventInfo):
    pass
