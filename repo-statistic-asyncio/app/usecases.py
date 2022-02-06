import asyncio

from app.clients import GithubClient
from app.settings import GITHUB_TOKEN
from app.toys import stopwatches, async_stopwatches
from app.entities import ContributorsStatistic
from app.repo import Repo


@stopwatches
def get_commit_statistics(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
) -> ContributorsStatistic:
    stat = ContributorsStatistic()
    commits = Repo.get_repository_commits(
        github_client,
        organisation_name,
        repository_name,
    )
    stat.consume(commits)
    return stat


@async_stopwatches
async def get_commit_statistics_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
) -> ContributorsStatistic:
    stat = ContributorsStatistic()
    commits = await Repo.get_repository_commits_async(
        github_client,
        organisation_name,
        repository_name,
    )
    stat.consume(commits)
    return stat


async def main():
    organisation_name = "veler"
    repository_name = "DevToys"
    client = GithubClient(GITHUB_TOKEN)
    res = get_commit_statistics(
        client,
        organisation_name,
        repository_name,
    )
    print(res)
    async_res = await get_commit_statistics_async(
        client,
        organisation_name,
        repository_name,
    )
    print(async_res)


if __name__ == '__main__':
    asyncio.run(main())
