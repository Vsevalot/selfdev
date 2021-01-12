import unittest
import playrix


class playrixTest(unittest.TestCase):
    def test_is_valid_github_url(self):
        self.assertTrue(playrix.is_valid_github_url("https://github.com/COMPANY/REPOSITORY"))
        self.assertTrue(playrix.is_valid_github_url("https:/github.com/COMPANY/REPOSITORY"))
        self.assertTrue(playrix.is_valid_github_url("https:github.com/COMPANY/REPOSITORY"))
        self.assertRaises(AttributeError, playrix.is_valid_github_url, "https://NOTGITHUB.com/COMPANY/REPOSITORY")
        self.assertRaises(AttributeError, playrix.is_valid_github_url, "https://github.com/COMPANY/")
        self.assertRaises(AttributeError, playrix.is_valid_github_url, "https://github.com/COMPANY/COMPANY/REPOSITORY")


if __name__ == "__main__":
    unittest.main()
