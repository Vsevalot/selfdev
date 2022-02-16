from typing import Generator, NoReturn, Optional
from enum import Enum
from datetime import datetime

from app.typehints import IssueInfo
from app.clients import GithubClient


class IssueState(Enum):
    open = 'open'
    closed = 'closed'
    all = 'all'


def get_issues_params(
        state: IssueState,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
) -> dict[str, str]:
    params = {'state': state}
    if since:
        params['since'] = since.isoformat()
    if until:
        params['until'] = until.isoformat()
    return params


def get_repository_issues(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        state: IssueState = IssueState.all.value,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
) -> Generator[NoReturn, IssueInfo, NoReturn]:
    params = get_issues_params(state, since, until)
    issues = github_client.get_issues(
        organisation_name,
        repository_name,
        **params,
    )
    for issue in issues:
        yield IssueInfo(**issue)


async def get_repository_issues_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        state: IssueState = IssueState.all.value,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
) -> list[IssueInfo]:
    params = get_issues_params(state, since, until)
    issues = github_client.get_issues_async(
        organisation_name,
        repository_name,
        **params,
    )
    return [IssueInfo(**issue) for issue in await issues]
