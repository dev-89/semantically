SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/"
PARTNER_SCHOLAR_URL = "https://partner.semanticscholar.org/v1"
API_PREFIX = "graph/v1/"
API_KEY = ""

ALLOWED_PAPER_URLs = []
ALLOWED_PAPER_ID_PRE = []

PAPER_TITLE_BOUNDARY = 0.9

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 100
DEFAULT_PAPER_FIELDS = ["paperId", "title"]

ALL_PAPER_FIELDS = [
    "paperId",
    "externalIds",
    "url",
    "title",
    "abstract",
    "venue",
    "year",
    "referenceCount",
    "citationCount",
    "isOpenAccess",
    "fieldsOfStudy",
    "authors",
]

ALL_DETAILED_AUTHOR_FIELDS = [
    "authorId",
    "externalIds",
    "url",
    "name",
    "aliases",
    "affiliations",
    "homepage",
    "paperCount",
    "citationCount",
    "hIndex",
    "papers",
]

ALL_DETAILED_PAPER_FIELDS = []

DEFAULT_AUTHOR_FIELDS = ["authorId", "name"]

VALID_ID_PREFIXES = ["CorpusId", "DOI", "ARXIV", "MAG", "ACL", "PMID", "PMCID", "URL"]

VALID_URL_LIST = [
    "semanticscholar.org",
    "arxiv.org",
    "aclweb.org",
    "acm.org",
    "biorxiv.org",
]
