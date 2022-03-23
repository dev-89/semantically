"""Semantically

Semantically is a Python library designed to easily retrieve data from Semantic Scholar. All data
is typed in dataclasses built around the Semantic Scholar API. Furthermore semantically supports
methods to retrieve papers by their title in order.
For larger requests semantically offers methods to retrieve papers according to lists of keywords.
In the background these requests are run asynchronously so that several requests can be sent in a
short amount of time.
"""

from typing import Dict, List, Union

import dacite
import Levenshtein as lh

from . import async_request, client, config, datastructures, exceptions, request


class Semantically:
    """Main interface for semantically library"""

    def __init__(
        self, raise_on_empty_result: bool = True, api_key: str = config.API_KEY
    ):
        self._client: client.SemanticClient = client.SemanticClient(key=api_key)
        self.request: request.SemanticRequest = request.SemanticRequest(self._client)
        self.raise_on_empty_result = raise_on_empty_result

        self.total: int = 0
        self.offset: int = 0
        self.next: int = 0

    def get_paper_by_title(
        self,
        paper_title: str,
        fields: List[str] = config.ALL_PAPER_FIELDS,
    ):
        """queries the paper for a given title. Each response of Semantic Scholar is checked to see, if
        the papers have a high Levenshtein ratio and the paper with the best match is returned.

        Args:
            paper_title (str): title of the queried paper
            fields (List[str], optional): fields of paper which should be returned. Defaults to config.ALL_PAPER_FIELDS.

        Returns:
            [type]: [description]
        """
        params = self._build_params(
            fields,
            offset=config.DEFAULT_OFFSET,
            limit=config.DEFAULT_LIMIT,
            query=paper_title,
        )
        new_params, data = self.request.query_paper(params)
        if not data:
            if self.raise_on_empty_result:
                raise exceptions.NoResultError(
                    paper_title, "Semantic Scholar returned no results for the query."
                )
            return None
        self.update_query_params(new_params)
        related_titles = [
            dacite.from_dict(data_class=datastructures.Paper, data=paper_dict)
            for paper_dict in data
            if self._is_title_equal(paper_title, paper_dict["title"])
        ]

        if not related_titles:
            if self.raise_on_empty_result:
                raise exceptions.NoResultError(
                    paper_title, "Semantic Scholar results did not match paper title."
                )
            return None

        sorted_list = sorted(
            related_titles,
            key=lambda d: self._is_title_equal(paper_title, d.title),
            reverse=True,
        )
        return sorted_list[0]

    def get_paper_by_keyword(
        self,
        keyword: str,
        offset: int = config.DEFAULT_OFFSET,
        limit: int = config.DEFAULT_LIMIT,
        fields: List[str] = config.DEFAULT_PAPER_FIELDS,
    ):
        """fetches paper according to a keyword. The ranking algorithm is described in
        https://medium.com/ai2-blog/building-a-better-search-engine-for-semantic-scholar-ea23a0b661e7

        Args:
            keyword (str): keyword query
            offset (int, optional): how many results should be skipped. Defaults to config.DEFAULT_OFFSET.
            limit (int, optional): how many results should be shown at once. Defaults to config.DEFAULT_LIMIT.
            fields (List[str], optional): paper fields to display. Defaults to config.DEFAULT_PAPER_FIELDS.
        """
        params = self._build_params(
            fields,
            offset=offset,
            limit=limit,
            query=keyword,
        )
        new_params, data = self.request.query_paper(params)
        if not data:
            if self.raise_on_empty_result:
                raise exceptions.NoResultError(
                    keyword, "Semantic Scholar returned no results for the query."
                )
            return None
        self.update_query_params(new_params)
        return [
            dacite.from_dict(data_class=datastructures.Paper, data=paper_dict)
            for paper_dict in data
        ]

    def get_papers_by_keyword(
        self,
        keywords: List[str],
        offset: int = config.DEFAULT_OFFSET,
        limit: int = config.DEFAULT_LIMIT,
        fields: List[str] = config.DEFAULT_PAPER_FIELDS,
    ):
        """fetches papers for each keyword in list. The ranking algorithm is described in
        https://medium.com/ai2-blog/building-a-better-search-engine-for-semantic-scholar-ea23a0b661e7

        Args:
            keyword (List[str]): keyword list query
            offset (int, optional): how many results should be skipped. Defaults to config.DEFAULT_OFFSET.
            limit (int, optional): how many results should be shown at once. Defaults to config.DEFAULT_LIMIT.
            fields (List[str], optional): paper fields to display. Defaults to config.DEFAULT_PAPER_FIELDS.
        """
        params = self._build_params(fields, offset=offset, limit=limit)
        async_semantic = async_request.SemanticAsyncRequest()
        returned_dict = async_semantic.query_paper(keywords, params)

        return self._type_dict(returned_dict, datastructures.Paper)

    def get_paper_by_id(
        self, paper_id: str, fields: List[str] = config.DEFAULT_PAPER_FIELDS
    ) -> datastructures.DetailedPaper:
        """fetches a paper according to its ID. Several ID types are accepted by the Semantic
        Scholar API and are documented under:
        https://api.semanticscholar.org/graph/v1#operation/get_graph_get_paper

        Args:
            paper_id (str): paper id in a valid format
            fields (List[str], optional): paper fields to display. Defaults to config.DEFAULT_PAPER_FIELDS.

        Returns:
            datastructures.DetailedPaper: paper with given paper id
        """
        data = self.request.get_paper_by_id(paper_id, fields)
        return dacite.from_dict(data_class=datastructures.DetailedPaper, data=data)

    def get_author_by_name(
        self,
        author_name: str,
        offset: int = config.DEFAULT_OFFSET,
        limit: int = config.DEFAULT_LIMIT,
        fields: List[str] = config.ALL_DETAILED_AUTHOR_FIELDS,
    ) -> Union[List[datastructures.DetailedAuthor], None]:
        """retrieves authors which hold the given author_name

        Args:
            author_name (str): name of author to be queried
            offset (int, optional): how many results should be skipped. Defaults to config.DEFAULT_OFFSET.
            limit (int, optional): how many results should be shown at once. Defaults to config.DEFAULT_LIMIT.
            fields (List[str], optional): author fields to display. Defaults to config.ALL_DETAILED_AUTHOR_FIELDS.

        Returns:
            List[datastructures.DetailedAuthor]: list of authors with given name
            None: if no result is returned and raise_on_empty_result is set to False
        """
        params = self._build_params(
            fields,
            offset=offset,
            limit=limit,
            query=author_name,
        )
        new_params, data = self.request.query_author(author_name, params)

        if not data:
            if self.raise_on_empty_result:
                raise exceptions.NoResultError(
                    author_name, "Semantic Scholar returned no results for the query."
                )
            return None

        self.update_query_params(new_params)
        return [
            dacite.from_dict(data_class=datastructures.DetailedAuthor, data=author_dict)
            for author_dict in data
        ]

    def get_authors_by_name(
        self,
        names: List[str],
        offset: int = config.DEFAULT_OFFSET,
        limit: int = config.DEFAULT_LIMIT,
        fields: List[str] = config.ALL_DETAILED_AUTHOR_FIELDS,
    ) -> Dict[str, List[datastructures.DetailedAuthor]]:
        """get several authors according to list of names

        Args:
            names (List[str]): names to be queried
            offset (int, optional): how many results should be skipped. Defaults to config.DEFAULT_OFFSET.
            limit (int, optional): how many results should be shown at once. Defaults to config.DEFAULT_LIMIT.
            fields (List[str], optional): author fields to display. Defaults to config.ALL_DETAILED_AUTHOR_FIELDS.

        Returns:
            Dict[str, List[datastructures.DetailedAuthor]]: mapping of queried names to results
        """
        params = self._build_params(fields, offset=offset, limit=limit)
        async_semantic = async_request.SemanticAsyncRequest()
        returned_dict = async_semantic.query_author(names, params)

        return self._type_dict(returned_dict, datastructures.DetailedAuthor)

    def get_author_by_id(
        self, author_id: str, fields: List[str] = config.ALL_DETAILED_AUTHOR_FIELDS
    ) -> datastructures.DetailedAuthor:
        """retrieves author according to semantic scholar id

        Args:
            author_id (str): semantic scholar id of author
            fields (List[str], optional): author fields to display. Defaults to config.ALL_DETAILED_AUTHOR_FIELDS.

        Returns:
            datastructures.DetailedAuthor: author info
        """
        data = self.request.get_paper_by_id(author_id, fields)
        return dacite.from_dict(data_class=datastructures.DetailedAuthor, data=data)

    def get_authors_by_id(
        self,
        author_id_list: List[str],
        fields: List[str] = config.ALL_DETAILED_AUTHOR_FIELDS,
    ) -> Dict[str, List[datastructures.DetailedAuthor]]:
        """gets several authors according to their semantic scholar id

        Args:
            author_id_list (List[str]): list of semantic scholar ids
            fields (List[str], optional): author fields to display. Defaults to config.ALL_DETAILED_AUTHOR_FIELDS.

        Returns:
            Dict[str, List[datastructures.DetailedAuthor]]: mapping between id and author info
        """
        params = self._build_params(fields)
        async_semantic = async_request.SemanticAsyncRequest()
        returned_dict = async_semantic.get_author_by_id(author_id_list, params)

        return self._type_dict(returned_dict, datastructures.DetailedAuthor)

    def update_query_params(self, new_params: datastructures.SemanticScholarParameter):
        self.offset = new_params.offset
        self.next = new_params.next
        self.total = new_params.total

    def _build_params(
        self,
        fields: List[str],
        offset: int = -1,
        limit: int = -1,
        query: str = "",
    ) -> Dict[str, str]:
        """build parameters for a Semantic Scholar query

        Args:
            fields (List[str]): list of fields to return
            offset (int, optional): query offset. Defaults to -1.
            limit (int, optional): how many results returned. Defaults to -1.
            query (str, optional): keyword, author name or paper title. Defaults to "".

        Returns:
            Dict[str, str]: parameter dict for query
        """
        query_dict = {}
        query_dict["fields"] = ",".join(fields)
        if offset >= 0:
            query_dict["offset"] = offset
        if limit >= 0:
            query_dict["limit"] = limit
        if query:
            query_dict["query"] = query
        return query_dict

    def _type_dict(self, dict_to_type: Dict, target_type) -> Dict:
        """types the values of the dictionary to target_type

        Args:
            dict_to_type (Dict): input dict of results
            target_type: type to cast to

        Returns:
            Dict: dict with target_type values
        """
        typed_dict = {}
        for key, value in dict_to_type.items():
            try:
                typed_dict[key] = [
                    dacite.from_dict(data_class=target_type, data=paper_dict)
                    for paper_dict in value
                ]
            except TypeError as te:
                if self.raise_on_empty_result:
                    raise te

        return typed_dict

    def _is_title_equal(self, title1: str, title2: str) -> bool:
        """checks if two titles are equal by computing the Levenshtein ratio and comparing
        it to a treshold defined in config.py

        Args:
            title1 (str): reference title
            title2 (str): title to be compared

        Returns:
            True: if Levenshtein distance is over a configured threshold
        """
        if lh.ratio(title1.lower(), title2.lower()) > config.PAPER_TITLE_BOUNDARY:
            return True
        return False
