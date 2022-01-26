from datetime import datetime
from typing import Optional

from app.exceptions import DateArgumentException


def get_time_period_string(
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
) -> str:
    match (since, until):
        case (None, None):
            return "for the all time"
        case (date1, None):
            return f"from {date1} to now"
        case (None, date2):
            return f"from the beginning to {date2}"
        case (date1, date2):
            return f"from {date1} to {date2}"
    raise ValueError()


def get_argument_date(date_str: str) -> datetime:
    formats = ('%Y-%m-%d', '%d.%m.%Y', '%d.%m.%y')
    for date_format in formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            pass
    raise DateArgumentException(date_str)
