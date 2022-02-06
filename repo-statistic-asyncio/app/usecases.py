import asyncio

from app.clients import GithubClient
from app.settings import GITHUB_TOKEN
from app.toys import stopwatches, async_stopwatches
from app.statistics import ContributorsStatistic, IssuesStatistic, PullRequestsStatistic
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


@stopwatches
def get_pull_request_statistics(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
) -> PullRequestsStatistic:
    pull_requests = Repo.get_repository_pulls(
        github_client,
        organisation_name,
        repository_name,
    )
    stat = PullRequestsStatistic(pull_requests)
    return stat


@async_stopwatches
async def get_pull_request_statistics_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
) -> PullRequestsStatistic:
    pull_requests = await Repo.get_repository_pulls_async(
        github_client,
        organisation_name,
        repository_name,
    )
    stat = PullRequestsStatistic(pull_requests)
    return stat


@stopwatches
def get_issues_statistics(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
) -> IssuesStatistic:
    issues = Repo.get_repository_issues(
        github_client,
        organisation_name,
        repository_name,
    )
    stat = IssuesStatistic(issues)
    return stat


@async_stopwatches
async def get_issues_statistics_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
) -> IssuesStatistic:
    issues = await Repo.get_repository_issues_async(
        github_client,
        organisation_name,
        repository_name,
    )
    stat = IssuesStatistic(issues)
    return stat

@async_stopwatches
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
    res_async = await get_commit_statistics_async(
        client,
        organisation_name,
        repository_name,
    )
    print(res_async)

    res = get_pull_request_statistics(
        client,
        organisation_name,
        repository_name,
    )
    print(res)
    res_async = await get_pull_request_statistics_async(
        client,
        organisation_name,
        repository_name,
    )
    print(res_async)

    res = get_issues_statistics(
        client,
        organisation_name,
        repository_name,
    )
    print(res)
    res_async = await get_issues_statistics_async(
        client,
        organisation_name,
        repository_name,
    )
    print(res_async)


if __name__ == '__main__':
    asyncio.run(main())
