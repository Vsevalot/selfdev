#!/usr/bin/python
import sys
import requests
import re
from typing import List
import datetime


def is_valid_github_repository_url(potential_url: str) -> bool:
    """
    Checks if the given URL is a valid github repository URL
        Args:
            potential_url (str): URL from user input
        Returns:
            (bool): True if the given URL is a valid github repository, False otherwise.
        Example:
            >>> is_valid_github_repository_url("https://github.com/COMPANY/REPOSITORY")
            True
            >>> is_valid_github_repository_url("https://NOTGITHUB.com/SOMETHING")
            False
    """
    regex = re.compile(r'https://github.com/[0-9a-zA-Z\-]+/[0-9a-zA-Z\-]+/?')
    if re.fullmatch(regex, potential_url):
        return True
    else:
        return False


def is_github_date(date_str: str) -> bool:
    """
    Checks if the given date has github date format: YYYY-MM-DD
        Args:
            date_str (str): date value as a string
        Returns:
            (bool) True if date_str has github date format, False otherwise.
        Examples:
            >>> is_github_date("2020-05-11")
            True
            >>> is_github_date("11.05.2020")
            False
    """
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def get_arg_dict(sys_args: List[str]) -> dict:
    """
    Parses script arguments to a dictionary with keys: url - URL (Always required) of a github repository.
    since (Optional) - date since analysis should be performed. Expected as YYYY-MM-DD.
    until (Optional) - date until analysis should be performed. Expected as YYYY-MM-DD.
    branch (Optional) - repository branch on which analysis should be performed.
    Always expects 3 and 4 argument as dates. If a date check failed assigns argument to the branch key.
        Args:
            sys_args (List[str]): list of script arguments - sys.argv
        Returns:
            args (dict): dict with filled values and None if optional argument was not in the sys_args
        Raises:
            ValueError: When fails to assign an argument from sys_args, raises value error
        Examples:
            >>> get_arg_dict(["file.py", "https://github.com/COMPANY/REPOSITORY"])
            {"url": "https://github.com/COMPANY/REPOSITORY", "since": None, "until": None, "branch": None}
            >>> get_arg_dict(["file.py", "https://github.com/COMPANY/REPOSITORY", "BRANCH_NAME"])
            {"url": "https://github.com/COMPANY/REPOSITORY", "since": None, "until": None, "branch": "BRANCH_NAME"}
            >>> get_arg_dict(["file.py", "https://github.com/COMPANY/REPOSITORY", "2020-12-27"])
    """
    if len(sys_args) < 2:  # Only file argument
        raise ValueError("Not enough arguments, you must specify repository URL as the first parameter")
    if len(sys_args) > 5:  # 1 - File argument, 2 - URL, 3 - first date, 4 - last date, 5 - branch, 6 ???
        raise ValueError("Too many arguments. The script expects: URL, date1 - optional, "
                         "date2 - optional, branch - optional")

    for arg in sys_args:
        if type(arg) is not str:
            raise ValueError(f"All elements of the {sys_args} must be str!")

    args = {"url": None, "since": None, "until": None, "branch": None}
    if is_valid_github_repository_url(sys_args[1]):
        args["url"] = sys_args[1]
    else:
        raise ValueError(f"Wrong URL {sys_args[1]}! Expected https://github.com/COMPANY/REPOSITORY pattern")

    if len(sys_args) == 3:  # file, URL and since/branch
        if is_github_date(sys_args[2]):
            args["since"] = sys_args[2]
        else:
            args["branch"] = sys_args[2]
    elif len(sys_args) > 3:  # file, URL, since ...
        if is_github_date(sys_args[2]):
            args["since"] = sys_args[2]
        else:
            raise ValueError(f"Wrong date format {sys_args[2]}! Expected YYYY-MM-DD")

        if len(sys_args) == 4:  # file, URL, since and until/branch
            if is_github_date(sys_args[3]):
                args["until"] = sys_args[3]
            else:
                args["branch"] = sys_args[3]
        elif len(sys_args) == 5:  # file, URL, since, until and branch
            if is_github_date(sys_args[3]):
                args["until"] = sys_args[3]
            else:
                raise ValueError(f"Wrong date format {sys_args[3]}! Expected YYYY-MM-DD")
            args["branch"] = sys_args[4]

    return args


if __name__ == "__main__":
    arg_dict = get_arg_dict(sys.argv)

    exit(0)
    url = "https://github.com/fastlane/fastlane"
    url = "https://api.github.com/repos/fastlane/fastlane/"
    payload = {"since": "2020-12-31", "page": 1, "per_page": 10}
    response = requests.get(url, timeout=1)
    response.raise_for_status()
    print(response.text)
