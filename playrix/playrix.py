import requests

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
    is_valid_github_url("123")
    exit(0)
    url = "https://github.com/fastlane/fastlane"
    url = "https://api.github.com/repos/fastlane/fastlane/"
    payload = {"since": "2020-12-31", "page": 1, "per_page": 10}
    response = requests.get(url)
    response.raise_for_status()
    print(response.text)