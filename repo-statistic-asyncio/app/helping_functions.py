from datetime import datetime

from app.exceptions import DateArgumentException


def get_argument_date(date_str: str) -> datetime:
    formats = ('%Y-%m-%d', '%d.%m.%Y', '%d.%m.%y')
    for date_format in formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            pass
    raise DateArgumentException(date_str)
