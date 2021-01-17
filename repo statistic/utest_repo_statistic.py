#!/usr/bin/python

import unittest
import repo_statistic
import datetime


class RepoStatisticTest(unittest.TestCase):
    def test_is_valid_github_url(self):
        self.assertTrue(repo_statistic.is_valid_github_repository_url("https://github.com/OWNER/REPOSITORY"))
        self.assertTrue(repo_statistic.is_valid_github_repository_url("https://github.com/OWNER/REPOSITORY/"))
        self.assertFalse(repo_statistic.is_valid_github_repository_url(""))
        self.assertFalse(repo_statistic.is_valid_github_repository_url("https:/github.com/OWNER/REPOSITORY"))
        self.assertFalse(repo_statistic.is_valid_github_repository_url("https:github.com/OWNER/REPOSITORY"))
        self.assertFalse(repo_statistic.is_valid_github_repository_url("https://github.com\\OWNER/REPOSITORY"))
        self.assertFalse(repo_statistic.is_valid_github_repository_url("https://NOTGITHUB.com/OWNER/REPOSITORY"))
        self.assertFalse(repo_statistic.is_valid_github_repository_url("https://github.com/OWNER/"))
        self.assertFalse(repo_statistic.is_valid_github_repository_url("https://github.com/OWNER/REPOSITORY/SOMETHING"))

    def test_is_valid_github_date(self):
        self.assertTrue(repo_statistic.is_valid_github_date("2020-05-11"))
        self.assertTrue(repo_statistic.is_valid_github_date("2020-5-11"))
        self.assertTrue(repo_statistic.is_valid_github_date("2020-05-7"))
        self.assertFalse(repo_statistic.is_valid_github_date("20-05-11"))
        self.assertFalse(repo_statistic.is_valid_github_date("2020.05.11"))
        self.assertFalse(repo_statistic.is_valid_github_date("2020-99-11"))
        self.assertFalse(repo_statistic.is_valid_github_date("2020-05-99"))
        self.assertFalse(repo_statistic.is_valid_github_date("11.5.20"))
        self.assertFalse(repo_statistic.is_valid_github_date("11.05.2020"))
        self.assertFalse(repo_statistic.is_valid_github_date("11-05-2020"))
        self.assertFalse(repo_statistic.is_valid_github_date("2020   -05-    07"))
        self.assertFalse(repo_statistic.is_valid_github_date("asdfasfasf"))
        self.assertFalse(repo_statistic.is_valid_github_date(""))

    def test_get_commits_payload(self):
        test_dict = {"sha": "master", "per_page": 100, "page": 1}
        self.assertDictEqual(test_dict, repo_statistic.get_commits_payload(None, None, "master"))

        test_dict = {"sha": "BRANCH_NAME", "per_page": 100, "page": 1}
        self.assertDictEqual(test_dict, repo_statistic.get_commits_payload(None, None, "BRANCH_NAME"))

        test_dict = {"sha": "master", "since": "2020-12-27", "per_page": 100, "page": 1}
        self.assertDictEqual(test_dict, repo_statistic.get_commits_payload("2020-12-27", None, "master"))

        test_dict = {"sha": "master", "since": "2020-12-27", "until": "2021-05-01", "per_page": 100, "page": 1}
        self.assertDictEqual(test_dict, repo_statistic.get_commits_payload("2020-12-27", "2021-05-01", "master"))

        test_dict = {"sha": "BRANCH_NAME", "since": "2020-12-27", "per_page": 100, "page": 1}
        self.assertDictEqual(test_dict, repo_statistic.get_commits_payload("2020-12-27", None, "BRANCH_NAME"))

        test_dict = {"sha": "BRANCH_NAME", "since": "2020-12-27", "until": "2021-05-01", "per_page": 100, "page": 1}
        self.assertDictEqual(test_dict, repo_statistic.get_commits_payload("2020-12-27", "2021-05-01", "BRANCH_NAME"))

    def test_get_pr_payload(self):
        test_dict = {"base": "master", "per_page": 100, "page": 1, "state": "all"}
        self.assertDictEqual(test_dict, repo_statistic.get_pr_payload("master"))

        test_dict = {"base": "BRANCH_NAME", "per_page": 100, "page": 1, "state": "all"}
        self.assertDictEqual(test_dict, repo_statistic.get_pr_payload("BRANCH_NAME"))

    def test_get_time_period_string(self):
        test_time_period = "of all time"
        self.assertEqual(test_time_period, repo_statistic.get_time_period_string(None, None))

        test_time_period = "since 2020-12-27"
        self.assertEqual(test_time_period, repo_statistic.get_time_period_string("2020-12-27", None))

        test_time_period = "since 2020-12-27 until 2021-05-01"
        self.assertEqual(test_time_period, repo_statistic.get_time_period_string("2020-12-27", "2021-05-01"))

        test_time_period = "until 2021-05-01"
        self.assertEqual(test_time_period, repo_statistic.get_time_period_string(None, "2021-05-01"))

    def test_in_time_period(self):
        date_to_check = datetime.datetime.strptime("2020-12-27", "%Y-%m-%d")
        since_date = datetime.datetime.strptime("1994-12-27", "%Y-%m-%d")
        until_date = datetime.datetime.strptime("2000-12-27", "%Y-%m-%d")
        self.assertTrue(repo_statistic.in_time_period(date_to_check, None, None))
        self.assertTrue(repo_statistic.in_time_period(date_to_check, since_date, None))
        self.assertFalse(repo_statistic.in_time_period(date_to_check, None, until_date))
        self.assertFalse(repo_statistic.in_time_period(date_to_check, since_date, until_date))
        date_to_check = datetime.datetime.strptime("1998-12-27", "%Y-%m-%d")
        self.assertTrue(repo_statistic.in_time_period(date_to_check, None, until_date))


if __name__ == "__main__":
    unittest.main()
