from datetime import datetime
import re

from app.exceptions import DateArgumentException


GITHUB_REPO_PATTERN = r'https://github.com/' \
                      r'(?P<owner>[^/]+?)/(?P<repo>[^/]+)'


def get_argument_date(date_str: str) -> datetime:
    formats = ('%Y-%m-%d', '%d.%m.%Y', '%d.%m.%y')
    for date_format in formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            pass
    raise DateArgumentException(date_str)


def parse_url(url: str) -> tuple[str, str]:
    """
    Parses url to get owner and repository name.
    """
    match = re.search(GITHUB_REPO_PATTERN, url)
    if match:
        return match.group('owner'), match.group('repo')
    raise ValueError()
