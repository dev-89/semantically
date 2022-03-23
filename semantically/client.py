"""Client module for connecting to the Semantic Scholar API."""

from typing import Dict, Tuple
from urllib.parse import urljoin

import requests

from . import config


class SemanticClient:
    """The SemanticClient holds information about connecting to the Semantic Scholar
    API and runs the requests to the API.
    """

    def __init__(
        self,
        host: str = config.SEMANTIC_SCHOLAR_URL,
        key: str = config.API_KEY,
        api_prefix: str = config.API_PREFIX,
    ) -> None:
        self.api_url = urljoin(host, api_prefix)
        self.header = {}
        if key:
            self.header = {"x-api-key": key}
            self.api_url = urljoin(config.PARTNER_SCHOLAR_URL, api_prefix)

    def send_get_request(self, path: str, params: Dict[str, str]) -> Tuple[int, str]:
        """sends a get request to the Semantic Scholar API and returns the status code
        and response body as string

        Args:
            path (str): path to endpoint
            params (Dict[str, str]): parameters for request

        Returns:
            Tuple[int, str]: status code and response body
        """
        url = urljoin(self.api_url, path)
        resp = requests.get(url=url, params=params, headers=self.header)
        return resp.status_code, resp.text
