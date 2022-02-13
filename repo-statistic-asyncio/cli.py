import asyncio
from datetime import datetime

from app.clients import GithubClient
from app.settings import GITHUB_TOKEN
from app.toys import async_stopwatches
from app import usecases

@async_stopwatches
async def main():
    organisation_name = "veler"
    repository_name = "DevToys"
    client = GithubClient(GITHUB_TOKEN)
    since = datetime(2021, 1, 1)
    until = datetime(2022, 1, 1)
    branch = 'new-font'

    res = usecases.get_commit_statistics(
        client,
        organisation_name,
        repository_name,
        branch=branch,
        since=since,
        until=until,
    )
    print(res)
    res_async = await usecases.get_commit_statistics_async(
        client,
        organisation_name,
        repository_name,
        branch=branch,
        since=since,
        until=until,
    )
    print(res_async)

    res = usecases.get_pull_request_statistics(
        client,
        organisation_name,
        repository_name,
        since=since,
        until=until,
    )
    print(res)
    res_async = await usecases.get_pull_request_statistics_async(
        client,
        organisation_name,
        repository_name,
        since=since,
        until=until,
    )
    print(res_async)

    res = usecases.get_issues_statistics(
        client,
        organisation_name,
        repository_name,
        since=since,
        until=until,
    )
    print(res)
    res_async = await usecases.get_issues_statistics_async(
        client,
        organisation_name,
        repository_name,
        since=since,
        until=until,
    )
    print(res_async)


if __name__ == '__main__':
    asyncio.run(main())
