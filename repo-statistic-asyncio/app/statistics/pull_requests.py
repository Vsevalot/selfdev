from typing import Iterable, NoReturn

from app.typehints import PRInfo, _EventState


class PullRequestsStatistic:
    def __init__(
            self,
            pull_requests: Iterable[PRInfo],
    ) -> NoReturn:
        self._stat = {state: 0 for state in _EventState}
        self._consume(pull_requests)

    def _consume(
            self,
            pull_requests: Iterable[PRInfo],
    ) -> NoReturn:
        for pr in pull_requests:
            self._stat[pr.state] += 1

    def __repr__(self) -> str:
        res = "PR statistic:\n"
        for state, count in self._stat.items():
            res += f"{state}: {count}\n"
        return res
