from typing import Generator, NoReturn, Optional
from datetime import datetime

from app.typehints import CommitInfo
from app.clients import GithubClient


def _get_commits_params(
        branch: Optional[str],
        since: Optional[datetime],
        until: Optional[datetime],
) -> dict[str, str]:
    params = {}
    if branch:
        params['sha'] = branch
    if since:
        params['since'] = since.isoformat()
    if until:
        params['until'] = until.isoformat()
    return params


def get_repository_commits(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        branch: Optional[str],
        since: Optional[datetime],
        until: Optional[datetime],
) -> Generator[NoReturn, CommitInfo, NoReturn]:
    params = _get_commits_params(branch, since, until)
    commits = github_client.get_commits(
        organisation_name,
        repository_name,
        **params,
    )
    for c in commits:
        yield CommitInfo(**c)


async def get_repository_commits_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        branch: Optional[str],
        since: Optional[datetime],
        until: Optional[datetime],
) -> list[CommitInfo]:
    params = _get_commits_params(branch, since, until)
    commits = github_client.get_commits_async(
        organisation_name,
        repository_name,
        **params,
    )
    return [CommitInfo(**c) for c in await commits]
