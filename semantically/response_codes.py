"""Module for holding response codes used by Semantic Scholar API."""

from enum import IntEnum


class ResponseCode(IntEnum):
    """Enum class to hold response codes used by Semantic Scholar"""

    BAD_QUERY = 400
    NOT_FOUND = 404
