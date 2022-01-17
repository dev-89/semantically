"""This module handles the base classes for asynchronous requests
to Semantic Scholar. These are used for requests containing several
queries."""

import asyncio
from typing import Dict, List
from urllib import parse

import aiohttp

from . import config


class SemanticAsyncRequest:
    """This class is responsible for handling asynchronous requests made
    to semantic scholar. Asynchronous requests are made when a lot of requests
    should be sent at the same time. Since these requests are executed concurrently
    a lot of time is saved compared to making each request synchronously.
    """

    def __init__(
        self,
        host: str = config.SEMANTIC_SCHOLAR_URL,
        key: str = config.API_KEY,
        api_prefix: str = config.API_PREFIX,
    ) -> None:
        self.api_key: str = key
        self.api_url = parse.urljoin(host, api_prefix)
        self.header = {}

    def _query_builder(
        self, base: str, queries: List[str], params: Dict[str, str]
    ) -> List[str]:
        """builds the url for queries made to API.

        Args:
            base (str): either "author" or "paper"
            queries (List[str]): list of keywords/titles/names
            params (Dict[str, str]): mapping of parameter key to value

        Returns:
            List[str]: list of formatted urls
        """
        urls = []
        for query in queries:
            params["query"] = query
            query_string = parse.urlencode(params)
            urls.append(f"{self.api_url}{base}/search?{query_string}")

        return urls

    def _id_builder(
        self, base: str, id_list: List[str], params: Dict[str, str], suffix: str = ""
    ) -> List[str]:
        """builds the urls for id based requests made to API.

        Args:
            base (str): either "author" or "paper"
            id_list (List[str]): list of author/paper ids
            params (Dict[str, str]): mapping of parameter key to value
            suffix (str, optional): optional path parameter for after id. Defaults to "".

        Returns:
            List[str]: list of formatted urls
        """
        query_string = parse.urlencode(params)
        urls = []
        if suffix:
            suffix = f"/{suffix}"
        for paper_id in id_list:
            urls.append(f"{self.api_url}{base}/{paper_id}{suffix}?{query_string}")

        return urls

    def _async_to_sync(self, func: asyncio.Future) -> List:
        """runs event loop till finishes and returns gathered results

        Args:
            func (asyncio.Future): asnychronous function to be executed

        Returns:
            List: event loop results
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(func)

        return result

    def _link_data(
        self, keys: List[str], values: List[List[Dict]]
    ) -> Dict[str, List[Dict]]:
        """maps query strings or ids to their result

        Args:
            keys (List[str]): list of ids or queries
            values (List[List[Dict]]): list of API results

        Returns:
            Dict[str, List[Dict]]: mapping of id/query to result
        """
        return_dict = {}
        for key, value in zip(keys, values):
            return_dict[key] = value

        return return_dict

    async def _get_resource(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """gets resource from Semantic Scholar API

        Args:
            session (aiohttp.ClientSession):  aiohttp session
            url (str): API request url (Semantic Scholar only works with path and query parameters)

        Returns:
            Dict: result of API
        """
        async with session.get(url) as resp:
            resource = await resp.json()
            if "data" in resource:
                resource = resource["data"]
            return resource

    async def _run_session(self, urls: List[str]):
        """runs asynchronous session for several requests

        Args:
            urls (List[str]): list of API endpoints

        Returns:
            List: gathered API results
        """
        async with aiohttp.ClientSession() as session:

            tasks = []
            for url in urls:
                tasks.append(asyncio.ensure_future(self._get_resource(session, url)))

            resource_list = await asyncio.gather(*tasks)
        return resource_list

    def query_paper(
        self, queries: List[str], params: Dict[str, str]
    ) -> Dict[str, List]:
        """queries several papers either all by keyword or title

        Args:
            queries (List[str]): list of keywords/titles
            params (Dict[str, str]): mapping of parameter key to value

        Returns:
            Dict[str, List]: mapping of keyword/title to result
        """
        returned_list = []
        urls = self._query_builder("paper", queries, params)
        returned_list = self._async_to_sync(self._run_session(urls))

        return_dict = self._link_data(queries, returned_list)

        return return_dict

    def get_paper_by_id(
        self, id_list: List[str], params: Dict[str, str]
    ) -> Dict[str, List]:
        """get several papers by their id

        Args:
            id_list (List[str]): list of ids with accepted format
            params (Dict[str, str]): mapping of parameter key to value

        Returns:
            Dict[str, List]: mapping of id to result
        """
        urls = self._id_builder("paper", id_list, params, "")
        returned_list = self._async_to_sync(self._run_session(urls))
        return_dict = self._link_data(id_list, returned_list)
        return return_dict

    def query_author(
        self, queries: List[str], params: Dict[str, str]
    ) -> Dict[str, List]:
        """queries several authors by name

        Args:
            queries (List[str]): list of keywords/titles
            params (Dict[str, str]): mapping of parameter key to value

        Returns:
            Dict[str, List]: mapping of name to result
        """
        urls = self._query_builder("author", queries, params)
        returned_list = self._async_to_sync(self._run_session(urls))
        return_dict = self._link_data(queries, returned_list)
        return return_dict

    def get_author_by_id(
        self, id_list: List[str], params: Dict[str, str]
    ) -> Dict[str, List]:
        """queries several authors by id

        Args:
            id_list (List[str]): list of author semantic scholar ids
            params (Dict[str, str]): mapping of parameter key to value

        Returns:
            Dict[str, List]: mapping of id to result
        """
        urls = self._id_builder("author", id_list, params, "")
        returned_list = self._async_to_sync(self._run_session(urls))
        return_dict = self._link_data(id_list, returned_list)
        return return_dict
