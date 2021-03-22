from typing import Union
import datetime


def get_time_period_string(since: Union[str, None] = None,
                           until: Union[str, None] = None) -> str:
    """
    Generates time period in string form for the given arguments of the arg_dict
        Args:
            since (Union[str, None]): a string date
            until (Union[str, None]): a string date
        Returns:
            time_period (str): string representation of the given time period
        Examples:
            >>> get_time_period_string(None, None)
            of all time
            >>> get_time_period_string("2020-12-27", None)
            since 2020-12-27
            >>> get_time_period_string(until="2020-12-27")
            until 2020-12-27
            >>> get_time_period_string(since="2020-12-27", until="2020-12-27")
            since 2020-12-27 until 2021-01-15
    """
    time_period = "of all time"
    if (since is not None) and (until is not None):
        time_period = f"since {since} until {until}"
    elif since is not None:
        time_period = f"since {since}"
    elif until is not None:
        time_period = f"until {until}"
    return time_period


def in_time_period(date_to_check: datetime.datetime,
                   since_date: Union[datetime.datetime, None],
                   until_date: Union[datetime.datetime, None]) -> bool:
    """
    Checks if the date_to_check is in between since_date and until_date
        Args:
            date_to_check (datetime.datetime): date which should be checked
            since_date (datetime.datetime): minimal allowed value for
            date_to_check. If None - no minimal border
            until_date (datetime.datetime): maximal allowed value for
            date_to_check. If None - no maximal border
        Returns:
            (bool) : True if date_to_check is in between since_date and
            until_date, False otherwise
        Examples:
            >>> date_to_check = datetime.datetime.strptime("2020-12-27",
                                                           "%Y-%m-%d")
            >>> in_time_period(date_to_check,  None, None)
            True
            >>> since_date = datetime.datetime.strptime("1994-12-27",
                                                        "%Y-%m-%d")
            >>> in_time_period(date_to_check,  since_date, None)
            True
            >>> until_date = datetime.datetime.strptime("2000-12-27",
                                                        "%Y-%m-%d")
            >>> in_time_period(date_to_check,  since_date, until_date)
            False
    """
    if (since_date is not None) and (until_date is not None):
        return since_date <= date_to_check <= until_date
    elif since_date is not None:
        return since_date <= date_to_check
    elif until_date is not None:
        return date_to_check <= until_date
    else:  # No time borders - date_to_check is always in a period
        return True
