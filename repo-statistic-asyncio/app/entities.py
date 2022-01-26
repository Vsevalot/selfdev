from collections import defaultdict
from typing import NoReturn

from app.typehints import CommitType


class ContributorsStatistic:
    _login_column_width = 40
    _commits_column_width = 15

    def __init__(self):
        self._statistic = defaultdict(lambda: 0)

    def consume(
        self,
        commits_page: list[CommitType],
    ) -> NoReturn:
        for c in commits_page:
            author = c["author"]
            if author is None:
                author = {"login": None}
            committer = author["login"]
            self._statistic[committer] += 1

    def __repr__(self):
        res = f"{'Login':{self._login_column_width}} {'commits'}\n"
        for login, commits in self._statistic.items():
            if login is None:
                login = "Unknown users"
            res += f"{login:{self._login_column_width}} {commits}\n"
        return res
