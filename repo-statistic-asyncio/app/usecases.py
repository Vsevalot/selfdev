from typing import Union


def list_contributors(token: str, repo_url: str, branch: str,
                      since: Union[str, None], until: Union[str, None]):
    print("list_contributors")
