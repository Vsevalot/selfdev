from collections import defaultdict
from typing import NoReturn, Iterable, Optional
from datetime import datetime

from app.statistics.common import Statistic

from app.typehints import CommitInfo


class ContributorsStatistic(Statistic):
    _login_column_width = 30
    _commits_column_width = 13

    def __init__(
        self,
        organisation: str,
        repository: str,
        since: Optional[datetime],
        until: Optional[datetime],
        branch: Optional[str],
        top_n: int = 30,
    ):
        super().__init__(
            organisation=organisation,
            repository=repository,
            since=since,
            until=until,
        )
        self._branch = branch
        self._top_n = top_n
        self._statistic = defaultdict(lambda: 0)

    def consume(
        self,
        commits: Iterable[CommitInfo],
    ) -> NoReturn:
        for c in commits:
            login = c.get_contributor()
            self._statistic[login] += 1

    def __str__(self) -> str:
        res = (
            f"Top {self._top_n} contributors for: "
            f"{self._organisation}/{self._repository}\n"
        )
        if self._branch:
            res += f"Branch: {self._branch}\n"
        else:
            res += "Branch - main repository branch\n"
        res += f"Time period: {self._time_range}\n\n"
        res += f"{'Login':<{self._login_column_width}}|" \
               f"{'Commits made':>{self._commits_column_width}}\n"
        res += "_" * (self._login_column_width +
                      self._commits_column_width + 1) + "\n"

        sorted_statistic = sorted(
            self._statistic.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        count = 0
        for login, commits in sorted_statistic:
            res += f"{login:<{self._login_column_width}}|" \
                   f"{commits:>{self._commits_column_width}}\n"
            count += 1
            if count >= self._top_n:
                break
        return res
