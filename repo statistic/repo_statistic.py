#!/usr/bin/python
import requests
import re
import datetime
from typing import List, Tuple, Dict, Union
import argparse


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


def is_valid_github_date(date_str: str) -> bool:
    """
    Checks if the given date has github date format: YYYY-MM-DD
        Args:
            date_str (str): date value as a string
        Returns:
            (bool) True if date_str has github date format, False otherwise.
        Examples:
            >>> is_valid_github_date("2020-05-11")
            True
            >>> is_valid_github_date("11.05.2020")
            False
    """
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def get_time_period_string(since: Union[str, None] = None, until: Union[str, None] = None) -> str:
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


def get_commits_payload(since: Union[str, None], until: Union[str, None], branch: str) -> Dict[str, Union[str, int]]:
    """
    Creates payload for get commits request from github.api: List commits.
    Parameter per_page is set to 100 (max value). Parameter page is set to 1
        Args:
            since (str): a string date in form "YYYY-MM-DD" or None
            until (str): a string date in form "YYYY-MM-DD" or None
            branch (str): name of a branch in repository
        Returns:
            payload (Dict[str, Union[str, int]]) dictionary with parameters for List commits in github.api
        Examples:
            >>> get_commits_payload("2020-12-27", None, "master")
            {"sha": "master", "since": "2020-12-27", "per_page": 100, "page": 1}
    """
    payload = {"sha": branch, "per_page": 100, "page": 1}
    if since is not None:
        payload["since"] = since
    if until is not None:
        payload["until"] = until
    return payload


def get_server_date(words_date_str: str) -> datetime.datetime:
    """
    Tries to get a server date from response header. Standard github date is YYYY-MM-DD,
    but the server one is "Sun, 17 Jan 2021 20:18:17 GMT". Didn't find any docs so uses try - except for the
    entire algorithm. This should not be bad because this function runs only 2 times per sript run.
        Args:
            words_date_str (str): response header date
        Returns:
            server_date (datetime.datetime): server date if possible, else - local machine date
        Examples:
            >>> get_server_date("Sun, 17 Jan 2021 20:18:17 GMT")
            datetime.datetime(2021, 1, 17)
    """
    try:
        week_day, date = words_date_str.split(', ')  # 'Sun, 17 Jan 2021 20:18:17 GMT'
        day, month, year, time, timezone = date.split(' ')
        month_dict = {"Jan": "01", "Feb": "02", "March": "03",
                      "April": "04", "May": "05", "June": "06",
                      "July": "07", "Aug": "08", "Sept": "09",
                      "Oct": "10", "Nov": "11", "Dec": "12"}
        if month in month_dict:
            month = month_dict[month]
        else:  # Can't find github's month names, may be they are different
            month = str(datetime.datetime.now().month)
        server_date = datetime.datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
        return server_date
    except ValueError:
        return datetime.datetime.now()


def get_contributors_dict(get_url: str, payload: Dict[str, Union[str, int]], top: int = 30, vp: bool = True,
                          timeout: int = 10, auth: requests.auth.HTTPBasicAuth = None) -> List[Tuple[str, int]]:
    """
    Counts all commits and returns a list of the (top) most active contributors within given time period for
    the given branch. If number of contributors is less than top, returns data for all contributors.
    Uses List commits from github.api.
        Args:
            get_url (str): "https://api.github.com/repos/{owner}/{repository}/commits" format string
            payload (Dict[str, Union[str, int]]): dictionary with github.api: List commits parameters
            top (int): number of top required contributors
            vp (bool): visual progress. If True - print's a dot with each get request
            timeout (int): request timeout in seconds
            auth (requests.auth.HTTPBasicAuth): authorization from HTTPBasicAuth for GET requests
        Returns:
            top_contributors_sorted (List[Tuple[str, int]]): List of tuples (login, contributions),
            ordered by contributions
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> get_contributors_dict("https...", {"sha": "master", "since": "2015-12-27", "per_page": 100, "page": 1})
            [("login1", 155), ("login2", 143) ...]
    """
    top_contributors = {}
    while True:
        if vp:
            print('.', end='')  # Just a visualisation that the script is working
        response = requests.get(get_url, params=payload, timeout=timeout, auth=auth)
        if response.status_code == 404:
            repo = get_url.replace("https://api.github.com/repos", "https://github.com")[:-len(get_url.split('/')[-1])]
            raise requests.HTTPError(f"Error 404. Can't find repository: {repo} with branch: {payload['sha']}")
        raise_for_limit(response)
        response.raise_for_status()

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


def print_top_active(repo_url: str, since: Union[str, None] = None, until: Union[str, None] = None,
                     branch: str = "master", top: int = 30, vp: bool = True, timeout: int = 10,
                     auth: requests.auth.HTTPBasicAuth = None) -> None:
    """
    Print a table of the top contributors for the given branch and time period.
    If a number of contributors is less than top, prints data for all contributors.
        Args:
            repo_url (str): URL to a github repository
            since (str): a string date in form "YYYY-MM-DD" or None, default is None
            until (str): a string date in form "YYYY-MM-DD" or None, default is None
            branch (str): name of a branch in repository, default is "master"
            top (int): number of required contributors, defualt is 30
            vp (bool): visual progress. If True - print's a dot with each get request, default is True
            timeout (int): request timeout in seconds
            auth (requests.auth.HTTPBasicAuth): authorization from HTTPBasicAuth for GET requests
        Returns:
            None
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> print_top_active("https...")
            List of the most active contributors of all time for master
            Login                                      contributions
            --------------------------------------------------------
            login1                                              2394
            login2                                               133
            ...
    """
    owner = repo_url.split('/')[-2]
    repository = repo_url.split('/')[-1]
    payload = get_commits_payload(since, until, branch)
    get_url = f"https://api.github.com/repos/{owner}/{repository}/commits"
    top_contributors = get_contributors_dict(get_url, payload, top, vp, timeout, auth)

    time_period = get_time_period_string(since, until)
    if len(top_contributors) == 0:
        print(f"No contributors {time_period} for {branch}")
        return

    print(f"List of the most active contributors {time_period} for {branch}")
    print(f"{'Login':40s}{'contributions':13s}")
    print(53 * '-')
    for contributor in top_contributors:
        print(f"{contributor[0]:40s}{contributor[1]:13d}")


def get_pr_payload(branch: str) -> Dict[str, Union[str, int]]:
    """
    Creates payload for github.api: List pull requests for the given branch.
    Parameter per_page is set to 100 (max value). Parameter page is set to 1.
    Parameter state is set to all - opened and closed PR.
        Args:
            branch (str): a name of the repository branch
        Returns:
            payload (Dict[str, str]) dictionary with parameter name as keys and parameter values as values
        Examples:
            >>> get_pr_payload("master")
            {"base": "master", "per_page": 100, "page": 1, "state": "all"}
    """
    return {"base": branch, "per_page": 100, "page": 1, "state": "all"}


def print_pr_data(repo_url: str, since: Union[str, None] = None, until: Union[str, None] = None,
                  branch: str = "master", days_to_old: int = 30, vp: bool = True,
                  timeout: int = 10, auth: requests.auth.HTTPBasicAuth = None) -> None:
    """
    Print data for Pull Requests - PR of the given time period and the given branch.
        Args:
            repo_url (str): URL to a github repository
            since (str): a string date in form "YYYY-MM-DD" or None, default is None
            until (str): a string date in form "YYYY-MM-DD" or None, default is None
            branch (str): name of a branch in repository, default is "master"
            days_to_old (int): if an PR is created in the given time period and still
            be opened for days_to_old or more it's consider to be an old one. The default value is 30
            vp (bool): visual progress. If True - print's a dot with each get request, default is True
            timeout (int): request timeout in seconds
            auth (requests.auth.HTTPBasicAuth): authorization from HTTPBasicAuth for GET requests
        Returns:
            None
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> print_pr_data("https...")
            .................
            Pull request data since 2020-12-27 for master:
            Opened 155
            Closed 43
            Old: 17
    """
    payload = get_pr_payload(branch)
    pull_request_dict = get_issues_dict(repo_url, payload, since, until, pr_issue=True, days_to_old=days_to_old,
                                        vp=vp, timeout=timeout, auth=auth)
    time_period = get_time_period_string(since, until)
    print(f"Pull request data {time_period} for {branch}:")
    print(f"Opened: {pull_request_dict['opened']:13d}")
    print(f"Closed: {pull_request_dict['closed']:13d}")
    print(f"Old: {pull_request_dict['old']:16d}")


def get_issues_payload() -> Dict[str, Union[str, int]]:
    """
    Creates payload for github.api: List issues.
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


def reduce_date(long_str_date: str) -> str:
    """
    Reduce '2021-01-14T09:02:42Z' to '2021-01-14'
        Args:
            long_str_date (str): issue 'created_at' field value
        Returns:
            github_date (str): issue 'created_at' field value reduced to 'YYYY-MM-DD' form
        Examples:
            >>> reduce_date('2021-01-14T09:02:42Z')
            '2021-01-14'
    """
    return long_str_date.split('T')[0]


def get_issues_dict(repo_url: str, payload: Dict[str, Union[str, int]], since: Union[str, None] = None,
                    until: Union[str, None] = None, pr_issue: bool = False, days_to_old: int = 30, vp: bool = True,
                    timeout: int = 10, auth: requests.auth.HTTPBasicAuth = None) -> Dict[str, int]:
    """
    Counts all issues of the given time period.
    Returns a dictionary with number of opened, closed and old issues.
        Args:
            repo_url (str): URL to a github repository
            payload (Dict[str, Union[str, int]]): dictionary with github.api: List pull requests or List issues
            since (str): a string date in form "YYYY-MM-DD" or None, default is None
            until (str): a string date in form "YYYY-MM-DD" or None, default is None
            pr_issue (bool): interested only in pull requests, default False.
            If true github.api List pull requests payload is expected
            days_to_old (int): if an issue is created in the given time period and still
            be opened for days_to_old or more it's consider to be an old one. The default value is 30
            vp (bool): visual progress. If True - print's a dot with each get request, default is True
            timeout (int): request timeout in seconds
            auth (requests.auth.HTTPBasicAuth): authorization from HTTPBasicAuth for GET requests
        Returns:
            pull_request_dict (Dict[str, int]): Dictionary with keys: opened, closed, old
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> get_issues_dict("https...", {"base": "master", "per_page": 100, "page": 1})
            {"opened": 83, "closed": 50, "old": 4}
    """
    owner = repo_url.split('/')[-2]
    repository = repo_url.split('/')[-1]
    if pr_issue:
        get_url = f"https://api.github.com/repos/{owner}/{repository}/pulls"
    else:
        get_url = f"https://api.github.com/repos/{owner}/{repository}/issues"

    if since is not None:
        since_date = datetime.datetime.strptime(since, "%Y-%m-%d")
    else:
        since_date = None

    if until is not None:
        until_date = datetime.datetime.strptime(until, "%Y-%m-%d")
    else:
        until_date = None

    today_date = None
    issue_dict = {"opened": 0, "closed": 0, "old": 0}
    while True:
        if vp:
            print('.', end='')  # Just a visualisation that the script is working
        response = requests.get(get_url, params=payload, timeout=timeout, auth=auth)
        if response.status_code == 404:
            repo = get_url.replace("https://api.github.com/repos", "https://github.com")[:-len(get_url.split('/')[-1])]
            raise requests.HTTPError(f"Error 404. Can't find repository: {repo}")
        raise_for_limit(response)
        response.raise_for_status()

        if today_date is None:
            today_date = get_server_date(response.headers.get("date"))  # Current server date
        response_json = response.json()
        for issue in response_json:
            created_date = datetime.datetime.strptime(reduce_date(issue["created_at"]), "%Y-%m-%d")
            if in_time_period(created_date, since_date, until_date):
                issue_dict["opened"] += 1
                if issue["state"] == "open":
                    delta = today_date - created_date
                    if delta.days >= days_to_old:
                        issue_dict["old"] += 1

            if issue["closed_at"] is not None:
                closed_date = datetime.datetime.strptime(reduce_date(issue["closed_at"]), "%Y-%m-%d")
                if in_time_period(closed_date, since_date, until_date):
                    issue_dict["closed"] += 1

        if len(response_json) < payload["per_page"]:  # the number of elements is less than per_page - end reached
            break
        else:
            payload["page"] += 1
    if vp:
        print()
    return issue_dict


def print_issues_data(repo_url: str, since: Union[str, None] = None, until: Union[str, None] = None,
                      days_to_old: int = 14, vp: bool = True,
                      timeout: int = 10, auth: requests.auth.HTTPBasicAuth = None) -> None:
    """
    Print data for issues of the given time period. Uses github.api: List issues.
        Args:
            repo_url (str): URL to a github repository
            since (str): a string date in form "YYYY-MM-DD" or None
            until (str): a string date in form "YYYY-MM-DD" or None
            days_to_old (int): if an issue is created in the given time period and still
            be opened for days_to_old or more it's consider to be an old one. The default value is 14
            vp (bool): visual progress. If True - print's a dot with each get request
            timeout (int): request timeout in seconds
            auth (requests.auth.HTTPBasicAuth): authorization from HTTPBasicAuth for GET requests
        Returns:
            None
        Raises:
            HTTPError: any http errors from response.raise_for_status() - not a 2XX status code
            OutOfLimitError: raises when no requests to github.api remained
        Examples:
            >>> print_issues_data("https://...", "2020-12-27")
            .................
            Issues data since 2020-12-27:
            Opened 101
            Closed 38
            Old: 7
    """
    payload = get_issues_payload()
    issues_dict = get_issues_dict(repo_url, payload, since, until, days_to_old=days_to_old,
                                  vp=vp, timeout=timeout, auth=auth)
    time_period = get_time_period_string(since, until)
    print(f"Issues data {time_period}:")
    print(f"Opened: {issues_dict['opened']:13d}")
    print(f"Closed: {issues_dict['closed']:13d}")
    print(f"Old: {issues_dict['old']:16d}")


def check_args(script_args: argparse.Namespace) -> None:
    """
    Checks that all script argumets are allowed.
        Args:
            script_args (argparse.Namespace): Namespace of the script arguments.
        Returns:
            (None)
        Raises:
            ValueError: if wrong script argument passed, raises corresponding ValueError
        Examples:
            >>> check_args(script_args)
    """
    if not is_valid_github_repository_url(script_args.url):
        raise ValueError(f"Wrong github repository URL: {script_args.url}. "
                         f"Expected URL in form: https://github.com/OWNER/REPOSITORY. "
                         f"Run script with --help or -h flag for more information")
    if script_args.since is not None:
        if not is_valid_github_date(script_args.since):
            raise ValueError(f"Wrong date format {script_args.since}. Expected date in github in form YYYY-MM-DD. "
                             f"Run script with --help or -h flag for more information")
    if script_args.until is not None:
        if not is_valid_github_date(script_args.until):
            raise ValueError(f"Wrong date format {script_args.until}. Expected date in github in form YYYY-MM-DD. "
                             f"Run script with --help or -h flag for more information")
    if script_args.top_contributors < 0:
        raise ValueError(f"Number of required top contributors must be greater than 0. "
                         f"Run script with --help or -h flag for more information")
    if script_args.pr_days_to_old < 0:
        raise ValueError(f"Number of days for PR to considered old must be greater than 0. "
                         f"Run script with --help or -h flag for more information")
    if script_args.pr_days_to_old < 0:
        raise ValueError(f"Number of days for an issue to considered old must be greater than 0. "
                         f"Run script with --help or -h flag for more information")
    if script_args.request_timeout < 0:
        raise ValueError(f"Number of seconds for request timeout must be greater than 0. "
                         f"Run script with --help or -h flag for more information")


def get_script_args() -> argparse.Namespace:
    """
    Parses the script arguments. Run script with --help or -h frag for more information
        Returns:
            script_args (argparse.Namespace): Namespace of the script arguments.
        Raises:
            ValueError: if wrong script argument passed, raises corresponding ValueError
        Examples:
            >>> get_script_args()
            argparse.Namespace
    """
    parser = argparse.ArgumentParser(description="Statistic of repository contributors, pull requests and issues. "
                                                 "Collects statistic for contributors, PR and issues in "
                                                 "the given time period (optional) and "
                                                 "the given branch (default is master) - contributors and PR only")
    parser.add_argument("url", type=str, help="URL of a github repository. "
                                              "Expects URL in form https://github.com/OWNER/REPOSITORY")
    parser.add_argument("--since", "-s", type=str,
                        help="Since which date collect statistic for contributors and PR statistic. "
                             "Expects date in github form: YYYY-MM-DD. "
                             "If not set, collects statistic since first record/the big bang")
    parser.add_argument("--until", "-u", type=str,
                        help="Until which date collect statistic for contributors and PR statistic "
                             "Expects date in github form: YYYY-MM-DD. "
                             "If not set, collects statistic until last record/universe heat death")
    parser.add_argument("--branch", "-b", type=str, default="master",
                        help="Name of a branch for contributors and PR statistic, default - master")
    parser.add_argument("--username", "-un", type=str, help="You can pass your github username to authorize and "
                                                            "increase the number of request from 60 to 5000 per hour")
    parser.add_argument("--token", "-t", type=str, help="You can pass your personal github token to authorize and "
                                                        "increase the number of request from 60 to 5000 per hour")
    parser.add_argument("--top_contributors", "-tc", type=int, default=30,
                        help="Number of required top contributors. The default value is 30")
    parser.add_argument("--pr_days_to_old", "-pro", type=int, default=30,
                        help="If an PR is created in the given time period and still be opened for pr_days_to_old "
                             "or more it's consider to be an old one. The default value is 30")
    parser.add_argument("--issue_days_to_old", "-io", type=int, default=14,
                        help="If an issue is created in the given time period and still be opened for "
                             "issue_days_to_old or more it's consider to be an old one. The default value is 14")
    parser.add_argument("--request_timeout", "-rto", type=int, default=10,
                        help="Each request takes from 1 to inf seconds. If a server needs more time to respond, "
                             "you can modify number of seconds for request timeout. Default value is 10 seconds")
    parser.add_argument("--visual_progress", "-vp", type=bool, default=True,
                        help="Visual progress. Each request takes from 1 to inf seconds. To visualize that the script "
                             "is working prints a dot with each get request. The default value is True")

    script_args = parser.parse_args()
    check_args(script_args)
    return script_args


def get_authentication(script_args: argparse.Namespace) -> requests.auth.HTTPBasicAuth:
    """
    Tries to authorize with given username and token
        Args:
            script_args (argparse.Namespace): Namespace of the script arguments.
            Must have username and token fileds not None.
        Returns:
            authentication (requests.auth.HTTPBasicAuth): authentication object
        Examples:
            >>> get_authentication(args)
            requests.auth.HTTPBasicAuth
    """
    auth = requests.auth.HTTPBasicAuth(script_args.username, script_args.token)
    if args.username is None or args.token is None:
        return auth

    auth_response = requests.get(f"https://api.github.com/users/{script_args.username}", auth=auth)
    if auth_response.status_code == 404:
        raise requests.HTTPError(f"No user with {script_args.username} or given token")
    auth_response.raise_for_status()

    print(f"You're authorized as {auth_response.json()['login']}. "
          f"You have {auth_response.headers.get('X-RateLimit-Remaining')} requests left.")
    return auth


if __name__ == "__main__":
    args = get_script_args()
    authentication = get_authentication(args)

    print(f"Collecting data for {args.url} {get_time_period_string(args.since, args.until)}, {args.branch}")

    print("\nCollecting contributors data. It might take a few minutes.")
    print_top_active(repo_url=args.url, since=args.since, until=args.until, branch=args.branch,
                     top=args.top_contributors, vp=args.visual_progress, timeout=args.request_timeout,
                     auth=authentication)

    print("\nCollecting pull requests data. It might take a few minutes.")
    print_pr_data(repo_url=args.url, since=args.since, until=args.until, branch=args.branch,
                  days_to_old=args.pr_days_to_old, vp=args.visual_progress,
                  timeout=args.request_timeout, auth=authentication)

    print("\nCollecting issues data. It might take a few minutes.")
    print_issues_data(repo_url=args.url, since=args.since, until=args.until, days_to_old=args.issue_days_to_old,
                      vp=args.visual_progress, timeout=args.request_timeout, auth=authentication)
