from app.repo.commits import (
    get_repository_commits,
    get_repository_commits_async,
)

from app.repo.pulls import (
    get_repository_pulls,
    get_repository_pulls_async,
)


class Repo:
    get_repository_commits = get_repository_commits
    get_repository_commits_async= get_repository_commits_async
    get_repository_pulls = get_repository_pulls
    get_repository_pulls_async = get_repository_pulls_async
