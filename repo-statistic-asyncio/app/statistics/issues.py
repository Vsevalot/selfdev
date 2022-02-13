from typing import Iterable, NoReturn, Optional
from datetime import datetime, timezone

from app.typehints import IssueInfo, _EventState
from app.statistics.common import Statistic


class IssuesStatistic(Statistic):
    _state_column_width = 12
    _number_column_width = 7
    _str_head = 'Issues statistic for:'

    def __init__(
        self,
        organisation: str,
        repository: str,
        since: Optional[datetime],
        until: Optional[datetime],
        days_to_old: int = 14,
    ) -> NoReturn:
        super().__init__(organisation, repository, since, until)
        self._now = datetime.now(timezone.utc)
        self._days_to_old = days_to_old
        self._statistic = {state: 0 for state in _EventState} | {"old": 0}

    def consume(
        self,
        issues: Iterable[IssueInfo],
    ) -> NoReturn:
        for issue in issues:
            self._statistic[issue.state] += 1
            if self._is_old(issue):
                self._statistic["old"] += 1

    def _is_old(
        self,
        issue: IssueInfo,
    ) -> bool:
        if issue.state != _EventState.open:
            return False
        opened_for = (self._now - issue.created_at).days
        if opened_for > self._days_to_old:
            return True
        return False

    def __str__(self) -> str:
        res = f"{self._str_head} {self._organisation}/{self._repository}\n"
        res += f"Time period: {self._time_range}\n"
        res += (
            f"{'State':<{self._state_column_width}}|"
            f"{'Number':>{self._number_column_width}}\n"
        )
        res += (
            "_" * (self._state_column_width + self._number_column_width + 1)
            + "\n"
        )
        for state, number in self._stat.items():
            res += (
                f"{state:<{self._state_column_width}}|"
                f"{number:>{self._number_column_width}}\n"
            )
        return res
