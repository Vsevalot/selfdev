#!/usr/bin/python

import unittest
import playrix
import datetime


class playrixTest(unittest.TestCase):
    def test_is_valid_github_url(self):
        self.assertTrue(playrix.is_valid_github_repository_url("https://github.com/OWNER/REPOSITORY"))
        self.assertTrue(playrix.is_valid_github_repository_url("https://github.com/OWNER/REPOSITORY/"))
        self.assertFalse(playrix.is_valid_github_repository_url(""))
        self.assertFalse(playrix.is_valid_github_repository_url("https:/github.com/OWNER/REPOSITORY"))
        self.assertFalse(playrix.is_valid_github_repository_url("https:github.com/OWNER/REPOSITORY"))
        self.assertFalse(playrix.is_valid_github_repository_url("https://github.com\\OWNER/REPOSITORY"))
        self.assertFalse(playrix.is_valid_github_repository_url("https://NOTGITHUB.com/OWNER/REPOSITORY"))
        self.assertFalse(playrix.is_valid_github_repository_url("https://github.com/OWNER/"))
        self.assertFalse(playrix.is_valid_github_repository_url("https://github.com/OWNER/REPOSITORY/SOMETHING"))

    def test_is_github_date(self):
        self.assertTrue(playrix.is_github_date("2020-05-11"))
        self.assertTrue(playrix.is_github_date("2020-5-11"))
        self.assertTrue(playrix.is_github_date("2020-05-7"))
        self.assertFalse(playrix.is_github_date("20-05-11"))
        self.assertFalse(playrix.is_github_date("2020.05.11"))
        self.assertFalse(playrix.is_github_date("2020-99-11"))
        self.assertFalse(playrix.is_github_date("2020-05-99"))
        self.assertFalse(playrix.is_github_date("11.5.20"))
        self.assertFalse(playrix.is_github_date("11.05.2020"))
        self.assertFalse(playrix.is_github_date("11-05-2020"))
        self.assertFalse(playrix.is_github_date("2020   -05-    07"))
        self.assertFalse(playrix.is_github_date("asdfasfasf"))
        self.assertFalse(playrix.is_github_date(""))

    def test_get_commits_payload(self):
        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": None, "until": None, "branch": None}
        test_dict = {"sha": "master", "per_page": 100, "page": 1}
        self.assertDictEqual(test_dict, playrix.get_commits_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": None, "until": None, "branch": "BRANCH_NAME"}
        test_dict = {"sha": "BRANCH_NAME", "per_page": 100, "page": 1}
        self.assertDictEqual(test_dict, playrix.get_commits_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27", "until": None, "branch": None}
        test_dict = {"sha": "master", "since": "2020-12-27", "per_page": 100, "page": 1}
        self.assertDictEqual(test_dict, playrix.get_commits_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                    "until": "2021-05-01", "branch": None}
        test_dict = {"sha": "master", "since": "2020-12-27", "until": "2021-05-01", "per_page": 100, "page": 1}
        self.assertDictEqual(test_dict, playrix.get_commits_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                    "until": None, "branch": "BRANCH_NAME"}
        test_dict = {"sha": "BRANCH_NAME", "since": "2020-12-27", "per_page": 100, "page": 1}
        self.assertDictEqual(test_dict, playrix.get_commits_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                    "until": "2021-05-01", "branch": "BRANCH_NAME"}
        test_dict = {"sha": "BRANCH_NAME", "since": "2020-12-27", "until": "2021-05-01", "per_page": 100, "page": 1}
        self.assertDictEqual(test_dict, playrix.get_commits_payload(arg_dict))

    def test_get_pulls_payload(self):
        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": None, "until": None, "branch": None}
        test_dict = {"base": "master", "per_page": 100, "page": 1, "state": "all"}
        self.assertDictEqual(test_dict, playrix.get_pulls_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": None, "until": None, "branch": "BRANCH_NAME"}
        test_dict = {"base": "BRANCH_NAME", "per_page": 100, "page": 1, "state": "all"}
        self.assertDictEqual(test_dict, playrix.get_pulls_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27", "until": None, "branch": None}
        test_dict = {"base": "master", "per_page": 100, "page": 1, "state": "all"}
        self.assertDictEqual(test_dict, playrix.get_pulls_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                    "until": "2021-05-01", "branch": None}
        test_dict = {"base": "master", "per_page": 100, "page": 1, "state": "all"}
        self.assertDictEqual(test_dict, playrix.get_pulls_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                    "until": None, "branch": "BRANCH_NAME"}
        test_dict = {"base": "BRANCH_NAME", "per_page": 100, "page": 1, "state": "all"}
        self.assertDictEqual(test_dict, playrix.get_pulls_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                    "until": "2021-05-01", "branch": "BRANCH_NAME"}
        test_dict = {"base": "BRANCH_NAME", "per_page": 100, "page": 1, "state": "all"}
        self.assertDictEqual(test_dict, playrix.get_pulls_payload(arg_dict))

    def test_get_time_period(self):
        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": None, "until": None, "branch": None}
        test_time_period = "of all time"
        self.assertEqual(test_time_period, playrix.get_time_period(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": None, "until": None, "branch": "BRANCH_NAME"}
        test_time_period = "of all time"
        self.assertEqual(test_time_period, playrix.get_time_period(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27", "until": None, "branch": None}
        test_time_period = "since 2020-12-27"
        self.assertEqual(test_time_period, playrix.get_time_period(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                    "until": "2021-05-01", "branch": None}
        test_time_period = "since 2020-12-27 until 2021-05-01"
        self.assertEqual(test_time_period, playrix.get_time_period(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                    "until": None, "branch": "BRANCH_NAME"}
        test_time_period = "since 2020-12-27"
        self.assertEqual(test_time_period, playrix.get_time_period(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                    "until": "2021-05-01", "branch": "BRANCH_NAME"}
        test_time_period = "since 2020-12-27 until 2021-05-01"
        self.assertEqual(test_time_period, playrix.get_time_period(arg_dict))

    def test_in_time_period(self):
        date_to_check = datetime.datetime.strptime("2020-12-27", "%Y-%m-%d")
        since_date = datetime.datetime.strptime("1994-12-27", "%Y-%m-%d")
        until_date = datetime.datetime.strptime("2000-12-27", "%Y-%m-%d")
        self.assertTrue(playrix.in_time_period(date_to_check, None, None))
        self.assertTrue(playrix.in_time_period(date_to_check, since_date, None))
        self.assertFalse(playrix.in_time_period(date_to_check, None, until_date))
        self.assertFalse(playrix.in_time_period(date_to_check, since_date, until_date))
        date_to_check = datetime.datetime.strptime("1998-12-27", "%Y-%m-%d")
        self.assertTrue(playrix.in_time_period(date_to_check, None, until_date))


if __name__ == "__main__":
    unittest.main()
