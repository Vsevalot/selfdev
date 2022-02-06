from typing import Generator, NoReturn

from app.typehints import CommitInfo
from app.clients import GithubClient


def get_repository_commits(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
) -> Generator[NoReturn, CommitInfo, NoReturn]:
    for c in github_client.get_commits(
        organisation_name,
        repository_name,
    ):
        yield CommitInfo(**c)


async def get_repository_commits_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
) -> list[CommitInfo]:
    commits = github_client.get_commits_async(
        organisation_name,
        repository_name,
    )
    return [CommitInfo(**c) for c in await commits]
