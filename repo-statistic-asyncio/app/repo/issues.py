from typing import Generator, NoReturn

from app.typehints import IssueInfo
from app.clients import GithubClient


def get_repository_issues(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
) -> Generator[NoReturn, IssueInfo, NoReturn]:
    for issue in github_client.get_issues(
        organisation_name,
        repository_name,
    ):
        yield IssueInfo(**issue)


async def get_repository_issues_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
) -> list[IssueInfo]:
    issues = github_client.get_issues_async(
        organisation_name,
        repository_name,
    )
    return [IssueInfo(**issue) for issue in await issues]
