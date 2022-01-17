"""This module holds all dataclasses, which are used and returned by Semantically"""

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
    authorId: str
    name: Optional[str]


@dataclass
class Citation:
    paperId: str
    url: Optional[str]
    title: Optional[str]
    venue: Optional[str]
    year: Optional[int]
    authors: Optional[List[Author]]


@dataclass
class Reference:
    paperId: str
    url: Optional[str]
    title: Optional[str]
    venue: Optional[str]
    year: Optional[int]
    authors: Optional[List[Author]]


@dataclass
class Paper:
    paperId: str
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
    authors: Optional[List[Author]]


@dataclass
class DetailedAuthor:
    authorId: str
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
    paperId: str
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
