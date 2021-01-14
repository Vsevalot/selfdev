#!/usr/bin/python

import sys
import requests
import datetime


if __name__ == "__main__":
    print(datetime.datetime.strptime("1120-05-11", '%Y-%m-%d'))

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