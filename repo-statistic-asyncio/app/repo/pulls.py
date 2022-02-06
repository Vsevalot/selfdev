from typing import Generator, NoReturn

from app.typehints import PRInfo
from app.clients import GithubClient


def get_repository_pulls(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
) -> Generator[NoReturn, PRInfo, NoReturn]:
    for pr in github_client.get_pulls(
        organisation_name,
        repository_name,
    ):
        yield PRInfo(**pr)


async def get_repository_pulls_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
) -> list[PRInfo]:
    pull_requests = github_client.get_pulls_async(
        organisation_name,
        repository_name,
    )
    return [PRInfo(**pr) for pr in await pull_requests]
