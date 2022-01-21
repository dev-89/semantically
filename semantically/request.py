"""This module handles all requests made to semantic scholar via the
Semantic client"""

import json
from typing import Dict, List, Tuple
from urllib import parse

from . import client, config, datastructures, exceptions
from . import response_codes as rc


class SemanticRequest:
    """SemanticRequest is a wrapper around SemanticClient to make predefined
    calls to the Semantic Scholar API to fetch information about papers or
    authors.
    """

    def __init__(self, semantic_client: client.SemanticClient):
        self._client = semantic_client

    def query_paper(
        self, params: Dict
    ) -> Tuple[datastructures.SemanticScholarParameter, List[Dict]]:
        """queries paper for either keyword or paper title

        Args:
            params(Dict): mapping of parameters for r equest

        Raises:
            exceptions.BadQueryError: query parameters did not match schema

        Returns:
            Tuple[datastructures.SemanticScholarParameter, Dict]: new Semantic Scholar
            parameters and List of paper data
        """
        code, resp = self._client.send_get_request("paper/search", params)

        if code == rc.ResponseCode.BAD_QUERY:
            raise exceptions.BadQueryError(
                params, "Query parameters do not match Semantic Scholar schema."
            )

        response_dict = json.loads(resp)
        new_parameters = datastructures.SemanticScholarParameter(
            response_dict.get("offset", 0),
            response_dict.get("limit", 0),
            response_dict.get("next", 0),
        )
        return new_parameters, response_dict.get("data", None)

    def get_paper_by_id(self, paper_id: str, fields: List[str]) -> Dict[str, str]:
        """queries the paper according to id

        Args:
            paper_id (str): id of paper
            fields (List[str]): fields to return

        Raises:
            exceptions.InvalidPaperIDError: paper id did not match expected format
            exceptions.BadQueryError: query parameters did not match schema
            exceptions.InvalidPaperIDError: paper id was not found

        Returns:
            Dict[str, str]: paper information
        """
        if not self.is_valid_paper_id(paper_id):
            raise exceptions.InvalidPaperIDError(
                paper_id, "The provided ID does not match any supported types."
            )
        params = self._build_params(fields)
        code, resp = self._client.send_get_request(f"paper/{paper_id}", params)

        if code == rc.ResponseCode.BAD_QUERY:
            raise exceptions.BadQueryError(
                params, "Query parameters do not match Semantic Scholar schema."
            )
        if code == rc.ResponseCode.NOT_FOUND:
            raise exceptions.InvalidPaperIDError(
                paper_id, "The paper could not be found."
            )

        response_dict = json.loads(resp)
        return response_dict

    def query_author(
        self, query_name: str, params: Dict
    ) -> Tuple[datastructures.SemanticScholarParameter, List[Dict]]:
        """queries author for name
        TODO: query_author and query_paper are basically identical => abstraction

        Args:
            query_name (str): name of the author
            fields (List[str]): list of fields to return
            offset (int): offset of returned items
            limit (int): amount of returned papers

        Raises:
            exceptions.BadQueryError: query parameters did not match schema

        Returns:
            Tuple[datastructures.SemanticScholarParameter, Dict]: new Semantic Scholar
            parameters and List of paper data
        """
        code, resp = self._client.send_get_request("author/search", params)

        if code == rc.ResponseCode.BAD_QUERY:
            raise exceptions.BadQueryError(
                params, "Query parameters do not match Semantic Scholar schema."
            )

        response_dict = json.loads(resp)
        new_parameters = datastructures.SemanticScholarParameter(
            response_dict.get("offset", 0),
            response_dict.get("limit", 0),
            response_dict.get("next", 0),
        )
        return new_parameters, response_dict["data"]

    def get_author_by_id(self, author_id: int, fields: List[str]) -> Dict[str, str]:
        """queries an author according to author id

        Args:
            author_id (int): id of author
            fields (List[str]): fields to return

        Raises:
            exceptions.BadQueryError: query parameters did not match schema
            exceptions.InvalidAuthorIDError: author id was not found

        Returns:
            Dict[str, str]: author information
        """
        params = self._build_params(fields)
        code, resp = self._client.send_get_request(f"author/{author_id}", params)

        if code == rc.ResponseCode.BAD_QUERY:
            raise exceptions.BadQueryError(
                params, "Query parameters do not match Semantic Scholar schema."
            )
        if code == rc.ResponseCode.NOT_FOUND:
            raise exceptions.InvalidAuthorIDError(
                author_id, "The author could not be found."
            )

        response_dict = json.loads(resp)
        return response_dict

    def is_valid_paper_id(self, to_check: str) -> bool:
        """checks if given id is accepted by Semantic Scholar API. For this the
        id needs to match any given criteria listed in the API documentation.

        Args:
            to_check (str): id which will be checked

        Returns:
            True: if id is valid
        """
        if self.is_sha(to_check):
            return True

        id_type = self.get_id_type(to_check)

        if not id_type:
            return False

        if id_type == "URL":
            return self.is_valid_url(to_check)

        return True

    def is_sha(self, to_check: str) -> bool:
        """checks if a str is SHA. For this the str needs to be 40 chars long and
        a hexadecimal number.

        Args:
            to_check (str): string to check if it is SHA

        Returns:
            True: if input is hexadecimal and 40 chars long
        """
        if len(to_check) != 40:
            return False
        try:
            int(to_check, 16)
        except ValueError:
            return False
        return True

    def get_id_type(self, to_check: str) -> str:
        """tries to retrieve id type based on strings prefix. If input does not match
        any id type an empty string is returned.

        Args:
            to_check (str): [description]

        Returns:
            str: [description]
        """
        for id_prefix in config.VALID_ID_PREFIXES:
            if id_prefix in to_check:
                return id_prefix
        return ""

    def is_valid_url(self, url: str) -> bool:
        """checks if given URL is allowed by Semantic Scholar API

        Args:
            url (str): [description]

        Returns:
            bool: [description]
        """
        parse_result = parse.urlparse(url)
        url_netloc = parse_result.netloc
        for valid_url in config.VALID_URL_LIST:
            if url_netloc == valid_url:
                return True
        return False
