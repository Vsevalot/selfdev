

def is_valid_github_url(raw_url: str) -> bool:
    """
    Checks if the given URL is a valid github repository URL
        Args:
            raw_url (str): URL from user input
        Returns:
            valid (str): True if the given URL is a valid one, False otherwise.
        Raises:
            AttributeError: If an empty argument given or raw_url is not a valid github repository URL.
        Example:
            is_valid_github_url("https://github.com/fastlane/fastlane") -> True
    """
    url = raw_url.replace('\\', '/')  # To be sure that / is the separator
    if len(url) == 0:
        raise AttributeError(f"Empty URL")

    if url[-1] == '/':  # from https://github.com/fastlane/fastlane/
        url = url[:-1]  # to https://github.com/fastlane/fastlane

    valid = True
    if url.startswith("https://github.com/"):
        pass
    elif url.startswith("https:/github.com/"):
        url = url.replace("https:/github.com", "https://github.com", 2)
    elif url.startswith("https:github.com/"):
        url = url.replace("https:github.com", "https://github.com", 1)
    else:
        valid = False

    url_parts = url.split('/')
    if len(url_parts) != 5:  # https://github.com/fastlane/fastlane case
        valid = False

    if not valid:
        raise AttributeError(f"{url} is not a valid github repository URL. Make sure that you're using "
                             f"https://github.com/COMPANY/REPOSITORY format")

    return valid


if __name__ == "__main__":
    url = "https:/github.com/COMPANY/REPOSITORY"
    if is_valid_github_url(url):
        print("It's okey to be gay!")

"""
USEFUL STAFF
https://towardsdatascience.com/github-user-insights-using-github-api-data-collection-and-analysis-5b7dca1ab214
https://devpractice.ru/unit-testing-in-python-part-1/
https://www.programiz.com/python-programming/docstrings
https://docs.github.com/en/free-pro-team@latest/rest/reference/repos#list-commits
"""