"""This module holds all dataclasses, which are used and returned by Semantically. The
structure of all data classes is derived from the Semantic Scholar API."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SemanticScholarParameter:
    offset: int = 0
    limit: int = 0
    next: int = 0
    total: int = 0


@dataclass
class Author:
    authorId: Optional[
        str
    ]  # note: even though it is always included it does not have to mean that the value is always not None
    name: Optional[str]


@dataclass
class Citation:
    paperId: Optional[str]
    url: Optional[str]
    title: Optional[str]
    venue: Optional[str]
    year: Optional[int]
    authors: Optional[List[Author]]


@dataclass
class Reference:
    paperId: Optional[
        str
    ]  # note: even though it is always included it does not have to mean that the value is always not None
    url: Optional[str]
    title: Optional[str]
    venue: Optional[str]
    year: Optional[int]
    authors: Optional[List[Author]]


@dataclass
class Paper:
    """Dataclass for semanticscholar paper query results. All given members are modeled after the Semantic
    Scholar API.
    """

    paperId: Optional[
        str
    ] = None  # note: even though it is always included it does not have to mean that the value is always not None
    externalIds: Optional[dict] = None
    url: Optional[str] = None
    title: Optional[str] = None
    abstract: Optional[str] = None
    venue: Optional[str] = None
    year: Optional[int] = None
    referenceCount: Optional[int] = None
    citationCount: Optional[int] = None
    influentialCitationCount: Optional[int] = None
    isOpenAccess: Optional[bool] = None
    fieldsOfStudy: Optional[List[str]] = None
    authors: Optional[List[Author]] = None


@dataclass
class DetailedAuthor:
    authorId: Optional[
        str
    ]  # note: even though it is always included it does not have to mean that the value is always not None
    externalIds: Optional[dict]
    url: Optional[str]
    name: Optional[str]
    aliases: Optional[List[str]]
    affiliations: Optional[List[str]]
    homepage: Optional[str]
    paperCount: Optional[int]
    citationCount: Optional[int]
    hIndex: Optional[int]
    papers: Optional[List[Paper]]


@dataclass
class DetailedPaper:
    paperId: Optional[
        str
    ]  # note: even though it is always included it does not have to mean that the value is always not None
    externalIds: Optional[dict]
    url: Optional[str]
    title: Optional[str]
    abstract: Optional[str]
    venue: Optional[str]
    year: Optional[int]
    referenceCount: Optional[int]
    citationCount: Optional[int]
    influentialCitationCount: Optional[int]
    isOpenAccess: Optional[bool]
    fieldsOfStudy: Optional[List[str]]
    authors: Optional[List[DetailedAuthor]]
    citations: Optional[List[Citation]]
    references: Optional[List[Reference]]
