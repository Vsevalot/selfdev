import asyncio
from datetime import datetime
import argparse

from app.clients import GithubClient
from app import usecases, validation, helping_functions
from app.toys import stopwatches, async_stopwatches
from app.exceptions import exception_handler, exception_handler_async

DAYS_TO_OLD = 30
TOP_N = 30


def get_script_args() -> argparse.Namespace:
    """
    Parses the script arguments. Run script with --help or -h flag
    for more information
        Returns:
            script_args (argparse.Namespace): Namespace of the script arguments
        Raises:
            ValueError: if wrong script argument passed,
            raises corresponding ValueError
        Examples:
            >>> get_script_args()
            argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="""Statistic of repository contributors, 
        pull requests and issues.
        Collects statistic for contributors, PR and issues in 
        the given time period (optional) and the given branch 
        (default is repo main branch) - contributors and PR only"""
    )
    parser.add_argument(
        "url",
        type=str,
        help="URL of a github repository. "
             "Expects URL in form https://github.com/OWNER/REPOSITORY",
    )
    parser.add_argument(
        "--since",
        "-s",
        default=None,
        type=str,
        help="Since which date collect statistic. "
             "Expects date in next forms: YYYY-MM-DD / DD.MM.YYYY / DD.MM.YY"
             ". Collects statistic since the big bang if not set",
    )
    parser.add_argument(
        "--until",
        "-u",
        type=str,
        help="Until which date collect statistic. "
             "Expects date in next forms: YYYY-MM-DD / DD.MM.YYYY / DD.MM.YY"
             ". Collects statistic until current time if not set",
    )
    parser.add_argument(
        "--branch",
        "-b",
        type=str,
        default=None,
        help="Name of a branch for contributors. Default - repo main branch",
    )
    parser.add_argument(
        "--token",
        "-t",
        type=str,
        help="Your personal github token to authorize and "
             "increase the number of request from 60 to 5000 per hour",
    )
    parser.add_argument(
        "--top_contributors",
        "-top_n",
        type=int,
        default=TOP_N,
        help=f"The number of top contributors to be printed. "
             f"Default value is {TOP_N}",
    )
    parser.add_argument(
        "--days_to_old",
        "-dto",
        type=int,
        default=DAYS_TO_OLD,
        help=f"If a PR/ISSUE is created in the given time period and still be "
             f"opened for this number of days or more, it's consider to be an "
             f"old one. The default value is {DAYS_TO_OLD}",
    )
    parser.add_argument(
        "-l",
        action='store_true',
        help=f"Collect statistic lazy. Works slower, "
             f"but consumes less memory",
    )

    script_args = parser.parse_args()
    validation.validate_args(script_args)
    return script_args


@exception_handler
@stopwatches
def main(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        since: datetime,
        until: datetime,
        branch: str,
        top_n: int,
        days_to_old: int,
):
    print(usecases.get_contributors_statistic(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
        branch=branch,
        top_n=top_n,
    ))
    print(usecases.get_pull_request_statistic(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
        days_to_old=days_to_old,
    ))
    print(usecases.get_issues_statistic(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
        days_to_old=days_to_old,
    ))


@exception_handler_async
@async_stopwatches
async def main_async(
        github_client: GithubClient,
        organisation_name: str,
        repository_name: str,
        since: datetime,
        until: datetime,
        branch: str,
        top_n: int,
        days_to_old: int,
):
    print(await usecases.get_contributors_statistic_async(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
        branch=branch,
        top_n=top_n,
    ))
    print(await usecases.get_pull_request_statistic_async(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
        days_to_old=days_to_old,
    ))
    print(await usecases.get_issues_statistic_async(
        github_client=github_client,
        organisation_name=organisation_name,
        repository_name=repository_name,
        since=since,
        until=until,
        days_to_old=days_to_old,
    ))


if __name__ == '__main__':
    args = get_script_args()
    client = GithubClient(args.token)

    _since = None
    if args.since:
        _since = helping_functions.get_argument_date(args.since)
    _until = None
    if args.until:
        _until = helping_functions.get_argument_date(args.until)
    organisation, repository = helping_functions.parse_url(args.url)

    if args.l:
        main(
            github_client=client,
            organisation_name=organisation,
            repository_name=repository,
            since=_since,
            until=_until,
            branch=args.branch,
            top_n=args.top_contributors,
            days_to_old=args.days_to_old,
        )
    else:
        asyncio.run(
            main_async(
                github_client=client,
                organisation_name=organisation,
                repository_name=repository,
                since=_since,
                until=_until,
                branch=args.branch,
                top_n=args.top_contributors,
                days_to_old=args.days_to_old,
            )
        )
