from app.repo.commits import (
    get_repository_commits,
    get_repository_commits_async,
)
from app.repo.pulls import (
    get_repository_pulls,
    get_repository_pulls_async,
)
from app.repo.issues import (
    get_repository_issues,
    get_repository_issues_async,
)

class Repo:
    get_repository_commits = get_repository_commits
    get_repository_commits_async= get_repository_commits_async
    get_repository_pulls = get_repository_pulls
    get_repository_pulls_async = get_repository_pulls_async
    get_repository_issues = get_repository_issues
    get_repository_issues_async = get_repository_issues_async
