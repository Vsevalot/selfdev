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


def get_commits_payload(arg_dict: Dict[str, Union[str, None]]) -> Dict[str, str]:
    """
    Creates payload for get commits request from script arguments in arg_dict.
    Parameter per_page is set to 100 (max value). Parameter page is set to 1
        Args:
            arg_dict (Dict[str, Union[str, None]): dictionary of script arguments - url, since, until, branch
        Returns:
            payload (Dict[str, str]) dictionary with parameter name as keys and parameter values as values
        Examples:
            >>> get_commits_payload({"url": "https...", "since": "2020-12-27", "until": None, "branch": None})
            {"sha": "master", "since": "2020-12-27", "per_page": 100, "page": 1}
    """
    payload = {"sha": "master", "per_page": 100, "page": 1}
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


def get_contributors_dict(get_url: str, payload: Dict[str, Union[str, int]],
                           top: int, vp: bool) -> List[Tuple[str, int]]:
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
            vp (bool): visual progress. If True - print's a dot with each get request
        Returns:
            top_contributors_sorted (List[Tuple[str, int]]): List of tuples (login, contributions),
            ordered by contributions
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> get_contributors_dict("https...", {"sha": "master", "since": "2015-12-27"})
            [(login1, number of contributions), (login2, number of contributions) ...]
    """
    top_contributors = {}
    while True:
        if vp:
            print('.', end='')  # Just a visualisation that the script is working
        response = requests.get(get_url, params=payload, timeout=10)
        response.raise_for_status()
        raise_for_limit(response)

        response_json = response.json()
        for commit in response_json:
            if commit["author"] is None:
                continue
            login = commit["author"]["login"]
            if login in top_contributors:
                top_contributors[login] += 1
            else:
                top_contributors[login] = 1

        if len(response_json) < payload["per_page"]:  # the number of commits is less than per_page - we reached the end
            break
        else:
            payload["page"] += 1
    if vp:
        print()
    top_contributors_sorted = sorted(top_contributors.items(), key=lambda item: item[1], reverse=True)
    return top_contributors_sorted[:top]


def get_time_period(arg_dict: Dict[str, Union[str, None]]) -> str:
    """
    Generates time period in string form for the given arguments of the arg_dict
        Args:
            arg_dict (Dict[str, Union[str, None]]): dictionary of script arguments - url, since, until, branch
        Returns:
            time_period (str)
        Examples:
            >>> get_time_period({"url": "https...", "since": "2020-12-27", "until": None, "branch": None})
            since 2020-12-27
            >>> get_time_period({"url": "https...", "since": None, "until": None, "branch": None})
            of all time
            >>> get_time_period({"url": "https...", "since": "2020-12-27", "until": "2021-01-15", "branch": None})
            since 2020-12-27 until 2021-01-15
    """
    time_period = "of all time"
    if (arg_dict["since"] is not None) and (arg_dict["until"] is not None):
        time_period = f"since {arg_dict['since']} until {arg_dict['until']}"
    elif arg_dict["since"] is not None:
        time_period = f"since {arg_dict['since']}"
    elif arg_dict["until"] is not None:
        time_period = f"until {arg_dict['until']}"
    return time_period


def print_top_active(arg_dict: Dict[str, Union[str, None]], top: int = 30, vp: bool = True) -> None:
    """
    Print a table of the top contributors for the given branch and time period.
    If number of contributors is less than top, prints data for all contributors.
        Args:
            arg_dict (Dict[str, Union[str, None]]): dictionary of script arguments - url, since, until, branch
            top (int): number of required contributors. The default value is 30
            vp (bool): visual progress. Default is True. If True - print's a dot with each get request
        Returns:
            None
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> print_top_active({"url": "https...", "since": "2020-12-27", "until": None, "branch": None})
            List of the most active contributors of all time for master
            Login                                      contributions
            --------------------------------------------------------
            login1                                              2394
            login2                                               133
            ...
    """
    owner = arg_dict["url"].split('/')[-2]
    repository = arg_dict["url"].split('/')[-1]
    payload = get_commits_payload(arg_dict)
    get_url = f"https://api.github.com/repos/{owner}/{repository}/commits"
    top_contributors = get_contributors_dict(get_url, payload, top, vp)

    time_period = get_time_period(arg_dict)
    if len(top_contributors) == 0:
        print(f"No contributors {time_period} for {payload['sha']}")
        return

    print(f"List of the most active contributors {time_period} for {payload['sha']}")
    print(f"{'Login':40s}{'contributions':13s}")
    print(53 * '-')
    for contributor in top_contributors:
        print(f"{contributor[0]:40s}{contributor[1]:13d}")


def get_pulls_payload(arg_dict: Dict[str, Union[str, None]]) -> Dict[str, Union[str, int]]:
    """
    Creates payload for get PR request from script arguments in arg_dict.
    Parameter per_page is set to 100 (max value). Parameter page is set to 1.
    Parameter state is set to all - opend and closed PR.
        Args:
            arg_dict (Dict[str, Union[str, None]): dictionary of script arguments - url, since, until, branch
        Returns:
            payload (Dict[str, str]) dictionary with parameter name as keys and parameter values as values
        Examples:
            >>> get_pulls_payload({"url": "https...", "since": "2020-12-27", "until": None, "branch": None})
            {"base": "master", "per_page": 100, "page": 1, "state": "all"}
    """
    payload = {"base": "master", "per_page": 100, "page": 1, "state": "all"}
    if arg_dict["branch"] is not None:
        payload["base"] = arg_dict["branch"]
    return payload


def in_time_period(date_to_check: datetime.datetime,
                   since_date: Union[datetime.datetime, None],
                   until_date: Union[datetime.datetime, None]) -> bool:
    """
    Checks if the date_to_check is in between since_date and until_date
        Args:
            date_to_check (datetime.datetime): date which should be checked
            since_date (datetime.datetime): minimal allowed value for date_to_check. If None - no minimal border
            until_date (datetime.datetime): maximal allowed value for date_to_check. If None - no maximal border
        Returns:
            (bool) : True if date_to_check is in between since_date and until_date, False otherwise
        Examples:
            >>> date_to_check = datetime.datetime.strptime("2020-12-27", "%Y-%m-%d")
            >>> in_time_period(date_to_check,  None, None)
            True
            >>> since_date = datetime.datetime.strptime("1994-12-27", "%Y-%m-%d")
            >>> in_time_period(date_to_check,  since_date, None)
            True
            >>> until_date = datetime.datetime.strptime("2000-12-27", "%Y-%m-%d")
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


def get_pull_requests_dict(arg_dict: Dict[str, Union[str, None]], days_to_old: int, vp: bool) -> Dict[str, int]:
    """
    Counts all Pull Requests - PR of the given time period and given branch.
    Returns a dictionary with number of opened, closed and old PR.
    Uses List pull requests from github.api.
        Args:
            arg_dict (Dict[str, Union[str, None]]): dictionary of script arguments - url, since, until, branch
            "since" key and "YYYY-MM-DD" format value.
            days_to_old (int): If an PR is created in the given time period and stil be opend 
            for days_to_old or more it's consider to be an old one
            vp (bool): visual progress. If True - print's a dot with each get request
        Returns:
            pull_request_dict (Dict[str, int]): Dictionary with keys: opened, closed, old
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> get_pull_requests_dict({"url": "https...", "since": "2020-12-27", "until": None, "branch": None}, 30)
            {"opened": 155, "closed": 43, "old": 13}
    """
    owner = arg_dict["url"].split('/')[-2]
    repository = arg_dict["url"].split('/')[-1]
    get_url = f"https://api.github.com/repos/{owner}/{repository}/pulls"
    payload = get_pulls_payload(arg_dict)

    since_date = None
    if arg_dict["since"] is not None:
        since_date = datetime.datetime.strptime(arg_dict["since"], "%Y-%m-%d")

    until_date = None
    if arg_dict["until"] is not None:
        until_date = datetime.datetime.strptime(arg_dict["until"], "%Y-%m-%d")

    today_date = datetime.datetime.now()
    pull_request_dict = {"opened": 0, "closed": 0, "old": 0}
    while True:
        if vp:
            print('.', end='')  # Just a visualisation that the script is working
        response = requests.get(get_url, params=payload, timeout=10)
        response.raise_for_status()
        raise_for_limit(response)

        response_json = response.json()
        for pr in response_json:
            created_date = datetime.datetime.strptime(pr["created_at"][:10], "%Y-%m-%d")
            if in_time_period(created_date, since_date, until_date):
                pull_request_dict["opened"] += 1
                if pr["state"] == "open":
                    delta = today_date - created_date
                    if delta.days >= days_to_old:
                        pull_request_dict["old"] += 1

            if pr["closed_at"] is not None:
                closed_date = datetime.datetime.strptime(pr["closed_at"][:10], "%Y-%m-%d")
                if in_time_period(closed_date, since_date, until_date):
                    pull_request_dict["closed"] += 1

        if len(response_json) < payload["per_page"]:  # the number of commits is less than per_page - we reached the end
            break
        else:
            payload["page"] += 1
    if vp:
        print()
    return pull_request_dict


def print_pull_request_data(arg_dict: Dict[str, Union[str, None]], days_to_old: int = 30, vp: bool = True) -> None:
    """
    Print data for Pull Requests - PR of the given time period and given branch.
        Args:
            arg_dict (Dict[str, Union[str, None]]): dictionary of script arguments - url, since, until, branch
            days_to_old (int): If an PR is created in the given time period and stil be opend 
            for days_to_old or more it's consider to be an old one. Default value 30
            vp (bool): visual progress. Default - True. If True - print's a dot with each get request
        Returns:
            None
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> print_pull_request_data({"url": "https...", "since": "2020-12-27", "until": None, "branch": None})
            .................
            Pull request data since 2020-12-27 for master:
            Opened 155
            Closed 43
            Old: 17
    """
    pull_request_dict = get_pull_requests_dict(arg_dict, days_to_old, vp)
    time_period = get_time_period(arg_dict)
    print(f"Pull request data {time_period} for {arg_dict['branch']}:")
    print(f"Opened: {pull_request_dict['opened']:13d}")
    print(f"Closed: {pull_request_dict['closed']:13d}")
    print(f"Old: {pull_request_dict['old']:16d}")


def get_issues_payload() -> Dict[str, Union[str, int]]:
    """
    Creates payload for get issues request.
    Parameter per_page is set to 100 (max value). Parameter page is set to 1.
    Parameter state is set to all - opend and closed issues.
        Args:
            (None)
        Returns:
            payload (Dict[str, str]) dictionary with parameter name as keys and parameter values as values
        Examples:
            >>> get_issues_payload()
            {"per_page": 100, "page": 1, "state": "all"}
    """
    return {"per_page": 100, "page": 1, "state": "all"}


def get_issues_dict(arg_dict: Dict[str, Union[str, None]], days_to_old: int, vp: bool) -> Dict[str, int]:
    """
    Counts all issues of the given time period.
    Returns a dictionary with number of opened, closed and old issues.
    Uses List issues from github.api.
        Args:
            arg_dict (Dict[str, Union[str, None]]): dictionary of script arguments - url, since, until, branch
            "since" key and "YYYY-MM-DD" format value.
            days_to_old (int): If an issues is created in the given time period and stil be opend
            for days_to_old or more it's consider to be an old one
            vp (bool): visual progress. If True - print's a dot with each get request
        Returns:
            pull_request_dict (Dict[str, int]): Dictionary with keys: opened, closed, old
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> get_issues_dict({"url": "https...", "since": "2020-12-27", "until": None, "branch": None}, 14)
            {"opened": 83, "closed": 50, "old": 4}
    """
    owner = arg_dict["url"].split('/')[-2]
    repository = arg_dict["url"].split('/')[-1]
    get_url = f"https://api.github.com/repos/{owner}/{repository}/issues"
    payload = get_issues_payload()

    since_date = None
    if arg_dict["since"] is not None:
        since_date = datetime.datetime.strptime(arg_dict["since"], "%Y-%m-%d")

    until_date = None
    if arg_dict["until"] is not None:
        until_date = datetime.datetime.strptime(arg_dict["until"], "%Y-%m-%d")

    today_date = datetime.datetime.now()
    issue_dict = {"opened": 0, "closed": 0, "old": 0}
    while True:
        if vp:
            print('.', end='')  # Just a visualisation that the script is working
        response = requests.get(get_url, params=payload, timeout=10)
        response.raise_for_status()
        raise_for_limit(response)

        response_json = response.json()
        for issue in response_json:
            created_date = datetime.datetime.strptime(issue["created_at"][:10], "%Y-%m-%d")
            if in_time_period(created_date, since_date, until_date):
                issue_dict["opened"] += 1
                if issue["state"] == "open":
                    delta = today_date - created_date
                    if delta.days >= days_to_old:
                        issue_dict["old"] += 1

            if issue["closed_at"] is not None:
                closed_date = datetime.datetime.strptime(issue["closed_at"][:10], "%Y-%m-%d")
                if in_time_period(closed_date, since_date, until_date):
                    issue_dict["closed"] += 1

        if len(response_json) < payload["per_page"]:  # the number of commits is less than per_page - we reached the end
            break
        else:
            payload["page"] += 1
    if vp:
        print()
    return issue_dict


def print_issues_data(arg_dict: Dict[str, Union[str, None]], days_to_old: int = 14, vp: bool = True) -> None:
    """
    Print data for issues of the given time period.
        Args:
            arg_dict (Dict[str, Union[str, None]]): dictionary of script arguments - url, since, until, branch
            days_to_old (int): If an issue is created in the given time period and stil be opend
             for days_to_old or more it's consider to be an old one. Default value 14
            vp (bool): visual progress. Default - True. If True - print's a dot with each get request
        Returns:
            None
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> print_issues_data({"url": "https...", "since": "2020-12-27", "until": None, "branch": None})
            .................
            Issues data since 2020-12-27:
            Opened 101
            Closed 38
            Old: 7
    """
    issues_dict = get_issues_dict(arg_dict, days_to_old, vp)
    time_period = get_time_period(arg_dict)
    print(f"Issues data {time_period}:")
    print(f"Opened: {issues_dict['opened']:13d}")
    print(f"Closed: {issues_dict['closed']:13d}")
    print(f"Old: {issues_dict['old']:16d}")


if __name__ == "__main__":
    arg_dict = get_arg_dict(sys.argv)
    print(f"Collecting data for {arg_dict['url']} {get_time_period(arg_dict)}:")
    print("Collecting contributors data. It might take a few minutes.")
    print_top_active(arg_dict)
    print("\nCollecting pull requests data. It might take a few minutes.")
    print_pull_request_data(arg_dict)
    print("\nCollecting issues data. It might take a few minutes.")
    print_issues_data(arg_dict)
