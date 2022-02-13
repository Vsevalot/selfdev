from datetime import datetime
from typing import Optional

from app.clients import GithubClient
from app.toys import stopwatches, async_stopwatches
from app.statistics import (
    ContributorsStatistic,
    IssuesStatistic,
    PullRequestsStatistic,
)
from app.repo import Repo


@stopwatches
def get_commit_statistics(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        branch: Optional[str] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
) -> ContributorsStatistic:
    commits = Repo.get_repository_commits(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        branch=branch,
        since=since,
        until=until,
    )
    stat = ContributorsStatistic()
    stat.consume(commits)
    return stat


@async_stopwatches
async def get_commit_statistics_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        branch: Optional[str] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
) -> ContributorsStatistic:
    commits = await Repo.get_repository_commits_async(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        branch=branch,
        since=since,
        until=until,
    )
    stat = ContributorsStatistic()
    stat.consume(commits)
    return stat


@stopwatches
def get_pull_request_statistics(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
) -> PullRequestsStatistic:
    pull_requests = Repo.get_repository_pulls(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
    )
    stat = PullRequestsStatistic(pull_requests)
    return stat


@async_stopwatches
async def get_pull_request_statistics_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
) -> PullRequestsStatistic:
    pull_requests = await Repo.get_repository_pulls_async(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
    )
    stat = PullRequestsStatistic(pull_requests)
    return stat


@stopwatches
def get_issues_statistics(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
) -> IssuesStatistic:
    issues = Repo.get_repository_issues(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
    )
    stat = IssuesStatistic(issues)
    return stat


@async_stopwatches
async def get_issues_statistics_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
) -> IssuesStatistic:
    issues = await Repo.get_repository_issues_async(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
    )
    stat = IssuesStatistic(issues)
    return stat
