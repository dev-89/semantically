"""This module holds all custom exceptions raised by Semantically."""

from typing import Dict


class BadQueryError(Exception):
    """This error is raised if an invalid query is sent to Semantic Scholar"""

    def __init__(self, query_url: Dict[str, str], message: str) -> None:
        self.query = query_url
        self.message = message
        super().__init__(message)


class InvalidPaperIDError(Exception):
    """This error is raised when the provided paper id is not valid"""

    def __init__(self, paper_id: str, message: str) -> None:
        self.paper_id = paper_id
        self.message = message
        super().__init__(message)


class InvalidAuthorIDError(Exception):
    """This error is raised when the provided author id is not valid"""

    def __init__(self, author_id: int, message: str) -> None:
        self.author_id = author_id
        self.message = message
        super().__init__(message)


class NoResultError(Exception):
    """This error is raised if raise_on_empty_result is set to True and Semantic
    Scholar retruns an empty response."""

    def __init__(self, request: str, message: str) -> None:
        self.request = request
        self.message = message
        super().__init__(message)
