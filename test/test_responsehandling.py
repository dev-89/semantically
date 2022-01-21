"""Here are all tests, which test how semantically handles Semantic Scholar responses"""

import pytest
import responses
from semantically import config, semantically

MISSING_AUTHOR_JSON = {
    "total": 4968079,
    "offset": 10,
    "next": 11,
    "data": [
        {
            "paperId": "aa3164f83e934896cdea31bf453b6bf97cda6fa3",
            "title": "Knowledge Graph Embedding for Link Prediction: A Comparative Analysis",
            "authors": [],
        }
    ],
}

MISSING_DATA_JSON = {
    "total": 0,
    "offset": 0,
    "next": 0,
    "data": [],
}

NO_DATA_JSON = {}


@responses.activate
def test_missing_all_data():
    responses.add(
        responses.GET,
        f"{config.SEMANTIC_SCHOLAR_URL}{config.API_PREFIX}paper/search?fields=paperId%2CexternalIds%2Curl%2Ctitle%2Cabstract%2Cvenue%2Cyear%2CreferenceCount%2CcitationCount%2CisOpenAccess%2CfieldsOfStudy%2Cauthors&offset=0&limit=100&query=random-id",
        json=NO_DATA_JSON,
        status=200,
    )

    tester = semantically.Semantically()
    with pytest.raises(semantically.exceptions.NoResultError):
        resp = tester.get_paper_by_title("random-id")


@responses.activate
def test_missing_data():
    responses.add(
        responses.GET,
        f"{config.SEMANTIC_SCHOLAR_URL}{config.API_PREFIX}paper/search?fields=paperId%2CexternalIds%2Curl%2Ctitle%2Cabstract%2Cvenue%2Cyear%2CreferenceCount%2CcitationCount%2CisOpenAccess%2CfieldsOfStudy%2Cauthors&offset=0&limit=100&query=random-id",
        json=MISSING_DATA_JSON,
        status=200,
    )

    tester = semantically.Semantically()
    with pytest.raises(semantically.exceptions.NoResultError):
        resp = tester.get_paper_by_title("random-id")


@responses.activate
def test_missing_return_data():
    responses.add(
        responses.GET,
        f"{config.SEMANTIC_SCHOLAR_URL}{config.API_PREFIX}paper/search?fields=paperId%2CexternalIds%2Curl%2Ctitle%2Cabstract%2Cvenue%2Cyear%2CreferenceCount%2CcitationCount%2CisOpenAccess%2CfieldsOfStudy%2Cauthors&offset=0&limit=100&query=Knowledge+Graph+Embedding+for+Link+Prediction:+A+Comparative+Analysis",
        json=MISSING_AUTHOR_JSON,
        status=200,
    )

    tester = semantically.Semantically()
    resp = tester.get_paper_by_title(
        "Knowledge Graph Embedding for Link Prediction: A Comparative Analysis"
    )

    assert resp.paperId == "aa3164f83e934896cdea31bf453b6bf97cda6fa3"
    assert resp.authors == []
