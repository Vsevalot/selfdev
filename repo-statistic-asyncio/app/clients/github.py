import aiohttp
import requests
import re
from typing import Generator, NoReturn, Optional

from app.typehints import HeadersType
from app.exceptions import raise_for_all


class GithubClient:
    _last_page_pattern = r'page=(?P<last_page>\d+)>; rel="last"'
    _page_param_name = "page"
    _relative_links_field_name = "link"
    _default_last_page = 1
    _base_path = "https://api.github.com"

    def __init__(
        self,
        token: Optional[str] = None,
    ):
        self._headers = {}
        if token:
            self._headers = {"Authorization": f"Bearer {token}"}

    def get_commits(
            self,
            organisation_name: str,
            repository_name: str,
            **kwargs,
    ) -> Generator[NoReturn, dict, NoReturn]:
        url = self._get_commits_url(organisation_name, repository_name)
        return self._get(url, **kwargs)

    async def get_commits_async(
            self,
            organisation_name: str,
            repository_name: str,
            **kwargs,
    ) -> list:
        url = self._get_commits_url(organisation_name, repository_name)
        return await self._get_async(url, **kwargs)

    def _get_commits_url(
            self,
            organisation_name: str,
            repository_name: str,
    ) -> str:
        return f'{self._base_path}/repos/' \
               f'{organisation_name}/{repository_name}/commits'

    def get_issues(
            self,
            organisation_name: str,
            repository_name: str,
            **kwargs,
    ) -> Generator[NoReturn, dict, NoReturn]:
        url = self._get_issues_url(organisation_name, repository_name)
        return self._get(url, **kwargs)

    async def get_issues_async(
            self,
            organisation_name: str,
            repository_name: str,
            **kwargs,
    ) -> list[dict]:
        url = self._get_issues_url(organisation_name, repository_name)
        return await self._get_async(url, **kwargs)

    def _get_issues_url(
            self,
            organisation_name: str,
            repository_name: str,
    ):
        return f'{self._base_path}/repos/' \
               f'{organisation_name}/{repository_name}/issues'

    def get_pulls(
            self,
            organisation_name: str,
            repository_name: str,
            **kwargs,
    ) -> Generator[NoReturn, dict, NoReturn]:
        url = self._get_pulls_url(organisation_name, repository_name)
        return self._get(url, **kwargs)

    async def get_pulls_async(
            self,
            organisation_name: str,
            repository_name: str,
            **kwargs,
    ) -> list[dict]:
        url = self._get_pulls_url(organisation_name, repository_name)
        return await self._get_async(url, **kwargs)
    
    def _get_pulls_url(
            self,
            organisation_name: str,
            repository_name: str,
    ) -> str:
        return f'{self._base_path}/repos/' \
               f'{organisation_name}/{repository_name}/pulls'

    def _get(
        self,
        url: str,
        **kwargs,
    ) -> Generator[NoReturn, dict, NoReturn]:
        response = requests.get(
            url,
            headers=self._headers,
            params=kwargs,
        )
        raise_for_all(response)
        for item in response.json():
            yield item

        last_page = self._get_last_page(response.headers)
        for page in range(2, last_page + 1):
            response = requests.get(
                url,
                params={self._page_param_name: page} | kwargs,
                headers=self._headers,
            )
            raise_for_all(response)
            for item in response.json():
                yield item

    async def _get_async(
            self,
            url: str,
            **kwargs,
    ) -> list[dict]:
        all_pages = []
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url,
                    params=kwargs,
                    headers=self._headers,
            ) as resp:
                raise_for_all(resp)
                page_data = await resp.json()
                all_pages.extend(page_data)
            last_page = self._get_last_page(resp.headers)

            for page in range(2, last_page + 1):
                async with session.get(
                    url,
                    params={self._page_param_name: page} | kwargs,
                    headers=self._headers,
                ) as resp:
                    raise_for_all(resp)
                    page_data = await resp.json()
                    all_pages.extend(page_data)
        return all_pages

    def _get_last_page(
            self,
            headers: HeadersType,
    ) -> int:
        """
        Get last page number from response headers.
        I know there are 'next' and 'links' fields in a request response,
        but I wanted to work with the 'link' header's field because
        the documentation tells only about this field
        """
        relative_links = headers.get(self._relative_links_field_name)
        if relative_links is None:
            return self._default_last_page

        last_page_match = re.search(self._last_page_pattern, relative_links)
        if last_page_match is None:
            return self._default_last_page
        return int(last_page_match.group("last_page"))
