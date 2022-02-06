import aiohttp
import requests
import re
from typing import Generator, NoReturn

from app.typehints import HeadersType


class GithubClient:
    _last_page_pattern = r'page=(?P<last_page>\d*)>; rel="last"'
    _page_param_name = "page"
    _relative_links_field_name = "link"
    _default_last_page = 1
    _base_path = "https://api.github.com"

    def __init__(
        self,
        token: str,
    ):
        self._token = token

    def get_commits(
            self,
            organisation_name: str,
            repository_name: str,
    ) -> Generator[NoReturn, dict, NoReturn]:
        url = f'{self._base_path}/repos/' \
              f'{organisation_name}/{repository_name}/commits'
        return self._get(url)

    async def get_commits_async(
            self,
            organisation_name: str,
            repository_name: str,
    ) -> list:
        url = f'{self._base_path}/repos/' \
              f'{organisation_name}/{repository_name}/commits'
        return await self._get_async(url)

    def _get(
        self,
        url: str,
    ) -> Generator[NoReturn, dict, NoReturn]:
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {self._token}"},
        )

        for c in response.json():
            yield c

        last_page = self._get_last_page(response.headers)
        for page in range(2, last_page + 1):
            response = requests.get(
                url,
                params={self._page_param_name: page},
                headers={"Authorization": f"Bearer {self._token}"},
            )
            for c in response.json():
                yield c

    async def _get_async(
            self,
            url: str,
    ) -> list:
        all_pages = []
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                page_data = await resp.json()
                all_pages.extend(page_data)
            last_page = self._get_last_page(resp.headers)

            for page in range(2, last_page + 1):
                async with session.get(
                    url,
                    params={self._page_param_name: page},
                    headers={"Authorization": f"Bearer {self._token}"},
                ) as resp:
                    page_data = await resp.json()
                    all_pages.extend(page_data)
        return all_pages

    def _get_last_page(
            self,
            headers: HeadersType,
    ) -> int:
        relative_links = headers.get(self._relative_links_field_name)
        result = re.search(self._last_page_pattern, relative_links)
        if result is None:
            return self._default_last_page
        return int(result.group("last_page"))
