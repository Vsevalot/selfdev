from typing import Optional
from datetime import datetime
from abc import ABC


class Statistic(ABC):
    _statistic: dict

    def __init__(
            self,
            organisation: str,
            repository: str,
            since: Optional[datetime],
            until: Optional[datetime],
    ):
        self._organisation = organisation
        self._repository = repository
        self._time_range = self._get_time_range_string(since, until)

    @classmethod
    def _get_time_range_string(
            cls,
            since: Optional[datetime],
            until: Optional[datetime],
    ) -> str:
        """
        Gives a string representation of the time range
        """
        match (since, until):
            case (None, None):
                return 'for all time'
            case (None, until):
                return f'until {until.strftime("%Y-%m-%d")}'
            case (since, None):
                return f'since {since.strftime("%Y-%m-%d")} to now'
            case (since, until):
                return f'since {since.strftime("%Y-%m-%d")} ' \
                       f'until {until.strftime("%Y-%m-%d")}'

    def get_statistic(self) -> dict:
        return self._statistic

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}' \
               f'(organisation={self._organisation}, ' \
               f'repository={self._repository}, ' \
               f'({self._time_range}){self._statistic}'
