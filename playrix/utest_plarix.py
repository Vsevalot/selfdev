#!/usr/bin/python

import unittest
import playrix


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

    def test_get_arg_dict(self):
        argv = ["file.py", "https://github.com/OWNER/REPOSITORY"]
        test_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": None, "until": None, "branch": None}
        self.assertDictEqual(test_dict, playrix.get_arg_dict(argv))

        argv = ["file.py", "https://github.com/OWNER/REPOSITORY", "BRANCH_NAME"]
        test_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": None,
                     "until": None, "branch": "BRANCH_NAME"}
        self.assertDictEqual(test_dict, playrix.get_arg_dict(argv))

        argv = ["file.py", "https://github.com/OWNER/REPOSITORY", "2020-12-27"]
        test_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                     "until": None, "branch": None}
        self.assertDictEqual(test_dict, playrix.get_arg_dict(argv))

        argv = ["file.py", "https://github.com/OWNER/REPOSITORY", "2020-12-27", "2021-05-01"]
        test_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                     "until": "2021-05-01", "branch": None}
        self.assertDictEqual(test_dict, playrix.get_arg_dict(argv))

        argv = ["file.py", "https://github.com/OWNER/REPOSITORY", "2020-12-27", "BRANCH_NAME"]
        test_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                     "until": None, "branch": "BRANCH_NAME"}
        self.assertDictEqual(test_dict, playrix.get_arg_dict(argv))

        argv = ["file.py", "https://github.com/OWNER/REPOSITORY", "2020-12-27", "2021-05-01", "BRANCH_NAME"]
        test_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                     "until": "2021-05-01", "branch": "BRANCH_NAME"}
        self.assertDictEqual(test_dict, playrix.get_arg_dict(argv))

        self.assertRaises(ValueError, playrix.get_arg_dict, [])
        self.assertRaises(ValueError, playrix.get_arg_dict, [True])
        self.assertRaises(ValueError, playrix.get_arg_dict, ["s1"])
        self.assertRaises(ValueError, playrix.get_arg_dict, ["s1", "s2", "s3", "s4", "s5", "s6"])
        self.assertRaises(ValueError, playrix.get_arg_dict, ["file.py", "https://NOTGITHUB.com/OWNER/REPOSITORY"])
        self.assertRaises(ValueError, playrix.get_arg_dict, ["file.py", "https://github.com/OWNER/REPOSITORY",
                                                             "INVALID DATE", "BRANCH_NAME"])
        self.assertRaises(ValueError, playrix.get_arg_dict, ["file.py", "https://github.com/OWNER/REPOSITORY",
                                                             "2020-12-27", "INVALID DATE", "BRANCH_NAME"])

    def test_get_commit_payload(self):
        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": None, "until": None, "branch": None}
        test_dict = {"sha": "master"}
        self.assertDictEqual(test_dict, playrix.get_commit_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": None, "until": None, "branch": "BRANCH_NAME"}
        test_dict = {"sha": "BRANCH_NAME"}
        self.assertDictEqual(test_dict, playrix.get_commit_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27", "until": None, "branch": None}
        test_dict = {"sha": "master", "since": "2020-12-27"}
        self.assertDictEqual(test_dict, playrix.get_commit_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                    "until": "2021-05-01", "branch": None}
        test_dict = {"sha": "master", "since": "2020-12-27", "until": "2021-05-01"}
        self.assertDictEqual(test_dict, playrix.get_commit_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                    "until": None, "branch": "BRANCH_NAME"}
        test_dict = {"sha": "BRANCH_NAME", "since": "2020-12-27"}
        self.assertDictEqual(test_dict, playrix.get_commit_payload(arg_dict))

        arg_dict = {"url": "https://github.com/OWNER/REPOSITORY", "since": "2020-12-27",
                    "until": "2021-05-01", "branch": "BRANCH_NAME"}
        test_dict = {"sha": "BRANCH_NAME", "since": "2020-12-27", "until": "2021-05-01"}
        self.assertDictEqual(test_dict, playrix.get_commit_payload(arg_dict))


if __name__ == "__main__":
    unittest.main()
