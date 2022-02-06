from typing import Union, Optional
from requests.models import CaseInsensitiveDict
from multidict import CIMultiDictProxy


HeadersType = Union[CaseInsensitiveDict, CIMultiDictProxy]


from pydantic import BaseModel


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
