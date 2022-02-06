from typing import Iterable, NoReturn

from app.typehints import IssueInfo, _EventState


class IssuesStatistic:
    _state_column_width = 20
    _number_column_width = 15

    def __init__(
            self,
            issues: Iterable[IssueInfo],
    ) -> NoReturn:
        self._issues = issues
        self._stat = {state: 0 for state in _EventState}
        self._consume(issues)

    def _consume(
            self,
            issues: Iterable[IssueInfo],
    ) -> NoReturn:
        for issue in issues:
            self._stat[issue.state] += 1

    def __repr__(self) -> str:
        res = 'Issue statistic:\n'
        for state, count in self._stat.items():
            res += f'{state:{self._state_column_width}}:' \
                   f'{count:{self._number_column_width}}\n'
        return res
