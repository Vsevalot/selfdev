from collections import defaultdict
from typing import NoReturn, Iterable

from app.typehints import CommitInfo


class ContributorsStatistic:
    _login_column_width = 40
    _commits_column_width = 15

    def __init__(self):
        self._statistic = defaultdict(lambda: 0)

    def consume(
        self,
        commits: Iterable[CommitInfo],
    ) -> NoReturn:
        for c in commits:
            login = c.get_contributor()
            self._statistic[login] += 1

    def __repr__(self) -> str:
        res = f"{'Login':{self._login_column_width}} {'commits'}\n"
        for login, commits in self._statistic.items():
            if login is None:
                login = "Unknown users"
            res += f"{login:{self._login_column_width}} {commits}\n"
        return res
