#!/usr/bin/python

import sys
import requests
import playrix


def get_commit_payload(arg_dict: dict) -> dict:
    """
    Creates payload for get commit request. Parameter per_page is set to 100 (max value). Parameter page
    is set to 1.
        Args:
            arg_dict (dict): dictionary of script arguments - url, since, until, branch
        Returns:
            payload (dict) dictionary with parameter names as keys and parameter values as values
        Examples:
            >>> get_commit_payload({"url": "https...", "since": "2020-12-27", "until": None, "branch": None})
            {"per_page": 100, "page": 1, "since": "2020-12-27", "sha": "master"}
    """
    payload = {"per_page": 100, "page": 1, "sha": "master"}
    if arg_dict["since"] is not None:
        payload["since"] = arg_dict["since"]
    if arg_dict["until"] is not None:
        payload["until"] = arg_dict["until"]
    if arg_dict["branch"] is not None:
        payload["sha"] = arg_dict["branch"]
    return payload


def print_the_most_active(arg_dict: dict) -> None:
    owner = arg_dict["url"].split('/')[-2]
    repository = arg_dict["url"].split('/')[-1]
    get_url = f"https://api.github.com/repos/{owner}/{repository}/commits"
    payload = get_commit_payload(arg_dict)
    response = requests.get(get_url, params=payload, timeout=10)
    response.raise_for_status()
    response_json = response.json()
    requests_remaining = response.headers.get("X-RateLimit-Remaining")
    login_commits = {}
    while len(response_json) > 0:
        for commit in response_json:
            login = commit["author"]["login"]
            if login in login_commits:
                login_commits[login] += 1
            else:
                login_commits[login] = 1
        payload["page"] += 1
        response = requests.get(get_url, params=payload, timeout=10)
        response.raise_for_status()
        response_json = response.json()

    print(requests_remaining)


if __name__ == "__main__":
    arg_dict = playrix.get_arg_dict(sys.argv)
    print(arg_dict)

    print_the_most_active(arg_dict)

    exit(0)
    url = "https://github.com/fastlane/fastlane"
    payload = {"since": "2020-12-31", "page": 1, "per_page": 10}
    response = requests.get(url, timeout=3)
    response.raise_for_status()
    print(response.text)

    print(sys.argv)

"""
USEFUL STAFF
https://towardsdatascience.com/github-user-insights-using-github-api-data-collection-and-analysis-5b7dca1ab214
https://devpractice.ru/unit-testing-in-python-part-1/
https://www.programiz.com/python-programming/docstrings
https://docs.github.com/en/free-pro-team@latest/rest/reference/repos#list-commits
"""