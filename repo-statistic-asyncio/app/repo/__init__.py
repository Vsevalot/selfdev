from app.repo.commits import (
    get_repository_commits,
    get_repository_commits_async,
)


class Repo:
    get_repository_commits = get_repository_commits
    get_repository_commits_async= get_repository_commits_async
