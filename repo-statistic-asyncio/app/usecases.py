from datetime import datetime
from typing import Optional

from app.clients import GithubClient
from app.statistics import (
    ContributorsStatistic,
    IssuesStatistic,
    PullRequestsStatistic,
)
from app.repo import Repo


def get_contributors_statistic(
    github_client: GithubClient,
    organisation_name: str,
    repository_name: str,
    branch: Optional[str],
    since: Optional[datetime],
    until: Optional[datetime],
    top_n: int,
) -> ContributorsStatistic:
    commits = Repo.get_repository_commits(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        branch=branch,
        since=since,
        until=until,
    )
    stat = ContributorsStatistic(
        organisation=organisation_name,
        repository=repository_name,
        branch=branch,
        since=since,
        until=until,
        top_n=top_n,
    )
    stat.consume(commits)
    return stat


async def get_contributors_statistic_async(
    github_client: GithubClient,
    organisation_name: str,
    repository_name: str,
    branch: Optional[str],
    since: Optional[datetime],
    until: Optional[datetime],
    top_n: int,
) -> ContributorsStatistic:
    commits = await Repo.get_repository_commits_async(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        branch=branch,
        since=since,
        until=until,
    )
    stat = ContributorsStatistic(
        organisation=organisation_name,
        repository=repository_name,
        branch=branch,
        since=since,
        until=until,
        top_n=top_n,
    )
    stat.consume(commits)
    return stat



def get_pull_request_statistic(
    github_client: GithubClient,
    organisation_name: str,
    repository_name: str,
    since: Optional[datetime],
    until: Optional[datetime],
    days_to_old: int,
) -> PullRequestsStatistic:
    pull_requests = Repo.get_repository_pulls(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
    )
    stat = PullRequestsStatistic(
        organisation=organisation_name,
        repository=repository_name,
        since=since,
        until=until,
        days_to_old=days_to_old,
    )
    stat.consume(pull_requests)
    return stat



async def get_pull_request_statistic_async(
    github_client: GithubClient,
    organisation_name: str,
    repository_name: str,
    since: Optional[datetime],
    until: Optional[datetime],
    days_to_old: int,
) -> PullRequestsStatistic:
    pull_requests = await Repo.get_repository_pulls_async(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
    )
    stat = PullRequestsStatistic(
        organisation=organisation_name,
        repository=repository_name,
        since=since,
        until=until,
        days_to_old=days_to_old,
    )
    stat.consume(pull_requests)
    return stat


def get_issues_statistic(
    github_client: GithubClient,
    organisation_name: str,
    repository_name: str,
    since: Optional[datetime],
    until: Optional[datetime],
    days_to_old: int,
) -> IssuesStatistic:
    issues = Repo.get_repository_issues(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
    )
    stat = IssuesStatistic(
        organisation=organisation_name,
        repository=repository_name,
        since=since,
        until=until,
        days_to_old=days_to_old,
    )
    stat.consume(issues)
    return stat



async def get_issues_statistic_async(
    github_client: GithubClient,
    organisation_name: str,
    repository_name: str,
    since: Optional[datetime],
    until: Optional[datetime],
    days_to_old: int,
) -> IssuesStatistic:
    issues = await Repo.get_repository_issues_async(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
    )
    stat = IssuesStatistic(
        organisation=organisation_name,
        repository=repository_name,
        since=since,
        until=until,
        days_to_old=days_to_old,
    )
    stat.consume(issues)
    return stat
