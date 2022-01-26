from app.settings import GITHUB_TOKEN
import fire
from typing import Union, NoReturn


def main(
        repo_url: str,
        branch: str = "master",
        since: Union[str, None] = None,
        until: Union[str, None] = None,
) -> NoReturn:
    print(f"URL: {repo_url}")
    print(f"Branch: {branch}")
    print(f"Time period: {get_time_period_string(since, until)}")
    list_contributors(GITHUB_TOKEN, repo_url, branch, since, until)


if __name__ == '__main__':
    repo_url_arg = "https://github.com/acidanthera/AppleALC"
    fire.Fire({"main": main}, ("main", repo_url_arg))
