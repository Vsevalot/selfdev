from typing import NoReturn, Optional
from datetime import datetime

from app.statistics.issues import IssuesStatistic


class PullRequestsStatistic(IssuesStatistic):
    def __init__(
            self,
            organisation: str,
            repository: str,
            since: Optional[datetime],
            until: Optional[datetime],
            days_to_old: int,
    ) -> NoReturn:
        super().__init__(organisation, repository, since, until, days_to_old)
        self._str_head = 'Pull requests statistic for:'

    def __str__(self):
        return super().__str__()
