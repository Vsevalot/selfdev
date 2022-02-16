from typing import Generator, NoReturn, Optional
from datetime import datetime

from app.typehints import PRInfo
from app.clients import GithubClient
from app.repo.issues import IssueState, get_issues_params


def get_repository_pulls(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        state: IssueState = IssueState.all.value,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
) -> Generator[NoReturn, PRInfo, NoReturn]:
    params = get_issues_params(state, since, until)
    pull_requests = github_client.get_pulls(
        organisation_name,
        repository_name,
        **params,
    )
    for pr in pull_requests:
        yield PRInfo(**pr)


async def get_repository_pulls_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        state: IssueState = IssueState.all.value,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
) -> list[PRInfo]:
    params = get_issues_params(state, since, until)
    pull_requests = github_client.get_pulls_async(
        organisation_name,
        repository_name,
        **params,
    )
    return [PRInfo(**pr) for pr in await pull_requests]
