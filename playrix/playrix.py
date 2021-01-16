#!/usr/bin/python
import sys
import requests
import re
import datetime
from typing import List, Tuple, Dict, Union


def is_valid_github_repository_url(potential_url: str) -> bool:
    """
    Checks if the given URL is a valid github repository URL
        Args:
            potential_url (str): URL from user input
        Returns:
            (bool): True if the given URL is a valid github repository, False otherwise.
        Example:
            >>> is_valid_github_repository_url("https://github.com/OWNER/REPOSITORY")
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
            >>> get_arg_dict(["file.py", "https://github.com/OWNER/REPOSITORY"])
            {"url": "https://github.com/OWNER/REPOSITORY", "since": None, "until": None, "branch": None}
            >>> get_arg_dict(["file.py", "https://github.com/OWNER/REPOSITORY", "BRANCH_NAME"])
            {"url": "https://github.com/OWNER/REPOSITORY", "since": None, "until": None, "branch": "BRANCH_NAME"}
            >>> get_arg_dict(["file.py", "https://github.com/OWNER/REPOSITORY", "2020-12-27"])
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
        raise ValueError(f"Wrong URL {sys_args[1]}! Expected https://github.com/OWNER/REPOSITORY pattern")

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


def get_commit_payload(arg_dict: Dict[str, Union[str, None]]) -> Dict[str, str]:
    """
    Creates payload for get commit request. Parameter per_page is set to 100 (max value). Parameter page
    is set to 1.
        Args:
            arg_dict (Dict[str, Union[str, None]): dictionary of script arguments - url, since, until, branch
        Returns:
            payload (Dict[str, str]) dictionary with parameter name as keys and parameter values as values
        Examples:
            >>> get_commit_payload({"url": "https...", "since": "2020-12-27", "until": None, "branch": None})
            {"sha": "master", "since": "2020-12-27"}
    """
    payload = {"sha": "master"}
    if arg_dict["since"] is not None:
        payload["since"] = arg_dict["since"]
    if arg_dict["until"] is not None:
        payload["until"] = arg_dict["until"]
    if arg_dict["branch"] is not None:
        payload["sha"] = arg_dict["branch"]
    return payload


class OutOfLimitError(Exception):
    pass


def raise_for_limit(response: requests.request) -> None:
    """
    Checks if the script ran out of requests. Github api gives 60 requests/hour for no authorized and
    5000/hour for authorized requests.
        Args:
            response(requests.request): response for a get request to github.api
        Returns:
            None
        Raises:
            OutOfLimitError: raises when no requests to github.api remaining
        Examples:
            >>> raise_for_limit(response)
            OutOfLimitError: You're out of requests, wait for an hour to get another 60 requests.

    """
    requests_remaining = int(response.headers.get("X-RateLimit-Remaining"))
    if requests_remaining == 0:
        raise OutOfLimitError(f"You're out of requests, wait for an hour"
                              f" to get another {response.headers.get('X-RateLimit-Limit')} requests.")


def get_top_contributors(get_url: str, payload: Dict[str, Union[str, int]], top: int) -> List[Tuple[str, int]]:
    """
    Gives a list of the (top) most active contributors of the all time for the given branch.
    Uses List contributors from github.api. If number of contributors is less than top,
    returns data for all contributors.
        Args:
            get_url (str): "https://api.github.com/repos/{owner}/{repository}/contributors" format string
            payload (Dict[str, Union[str, int]]): dictionary with "sha" key and branch name as value
            top (int): number of required contributors
        Returns:
            top_contributors (List[Tuple[str, int]]): List of tuples (login, contributions), ordered by contributions
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> get_top_contributors("https...", {"sha": "master"})
            [(login1, number of contributions), (login2, number of contributions) ...]
    """
    payload["page"] = 1  # Start from the first page, move to the next if required
    payload["per_page"] = top
    if payload["per_page"] > 100:  # 100 is the max for List contributors from github.api
        payload["per_page"] = 100
    top_contributors = []
    while True:
        response = requests.get(get_url, params=payload, timeout=10)
        response.raise_for_status()
        raise_for_limit(response)

        response_json = response.json()
        for contributor in response_json:
            top_contributors.append((contributor["login"], int(contributor["contributions"])))
        if len(top_contributors) >= top:
            break
        elif len(response_json) < payload["per_page"]:  # if so we reached the last page
            break
        else:
            payload["page"] += 1

    return top_contributors[:top]


def count_top_contributors(get_url: str, payload: Dict[str, Union[str, int]], top: int) -> list:
    """
    Counts all commits and returns a list of the (top) most active contributors
    within given time period for the given branch. If number of contributors is less than top,
    returns data for all contributors.
    Uses List commits from github.api.
        Args:
            get_url (str): "https://api.github.com/repos/{owner}/{repository}/commits" format string
            payload (Dict[str, Union[str, int]]): dictionary with "sha" key and branch name as value,
            "since" key and "YYYY-MM-DD" format value.
            top (int): number of required contributors
        Returns:
            top_contributors_sorted (List[Tuple[str, int]]): List of tuples (login, contributions),
            ordered by contributions
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> get_top_contributors("https...", {"sha": "master", "since": "2015-12-27"})
            [(login1, number of contributions), (login2, number of contributions) ...]
    """
    payload["page"] = 1  # Start from the first page, move to the next if required
    payload["per_page"] = 100  # 100 is the max for List commits from github.api
    top_contributors = {}
    while True:
        response = requests.get(get_url, params=payload, timeout=10)
        response.raise_for_status()
        raise_for_limit(response)

        response_json = response.json()
        for commit in response_json:
            login = commit["author"]["login"]
            if login in top_contributors:
                top_contributors[login] += 1
            else:
                top_contributors[login] = 1

        if len(response_json) < payload["per_page"]:  # the number of commits is less than per_page - we reached the end
            break
        else:
            payload["page"] += 1

    top_contributors_sorted = sorted(top_contributors.items(), key=lambda item: item[1], reverse=True)
    return top_contributors_sorted[:top]


def print_top_active(arg_dict: Dict[str, Union[str, None]], top: int = 30) -> None:
    """
    Print a table of the top contributors for the given branch and time period.
    If number of contributors is less than top, prints data for all contributors.
        Args:
            arg_dict (Dict[str, Union[str, None]]): dictionary of script arguments - url, since, until, branch
            top (int): number of required contributors
        Returns:
            None
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> print_top_active({"url": "https...", "since": "2020-12-27", "until": None, "branch": None})
                    List of the most active contributors
            Login                                      contributions
            --------------------------------------------------------
            login1                                              2394
            login2                                               133
            ...
    """
    owner = arg_dict["url"].split('/')[-2]
    repository = arg_dict["url"].split('/')[-1]
    payload = get_commit_payload(arg_dict)
    top_contributors = []
    if ("since" not in payload) and ("until" not in payload):  # If no dates specified just ask github
        get_url = f"https://api.github.com/repos/{owner}/{repository}/contributors"
        top_contributors = get_top_contributors(get_url, payload, top)
    else:
        get_url = f"https://api.github.com/repos/{owner}/{repository}/commits"
        top_contributors = count_top_contributors(get_url, payload, top)

    print("        List of the most active contributors")
    print(f"{'Login':40s}{'contributions':13s}")
    print(53 * '-')
    for contributor in top_contributors:
        print(f"{contributor[0]:40s}{contributor[1]:13d}")


if __name__ == "__main__":
    arg_dict = get_arg_dict(sys.argv)
    print_top_active(arg_dict)
