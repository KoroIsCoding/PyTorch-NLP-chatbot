# Authors: Koro_Is_Coding
# License: Apache v2.0

# standard libraries


# external libraries
import pytest
from io import StringIO

# module to be tested
from chatbot import SearchEngineStruct
from chatbot import SearchException


def test_se_default_init():
    """
    Test the default initialization of SearchEngineStruct.

    This test checks if the default attributes of the SearchEngineStruct object are set correctly.
    """
    se = SearchEngineStruct()
    assert se.google_api_key == "AIzaSyAGHYwrgMmAHlFwM-GmS2anQ7xWu7qcIjA"
    assert se.google_engine_key == "7a8bd65adc0b760d8"
    assert se.top_result == list()
    assert se.relevant == list()
    assert se.irrelevant == list()
    assert se.query == ""


def test_se_api_init():
    """
    Test the initialization of SearchEngineStruct with provided API keys.

    This test checks if the attributes of the SearchEngineStruct object are set correctly when
    the google_api_key and google_engine_key arguments are provided.
    """
    google_api_key = "api"
    google_engine_key = "engine"
    se = SearchEngineStruct(google_api_key, google_engine_key)
    assert se.google_api_key == "api"
    assert se.google_engine_key == "engine"
    assert se.top_result == list()
    assert se.relevant == list()
    assert se.irrelevant == list()
    assert se.query == ""


def test_get_top_result_empty():
    """
    Test the get_top_result method of SearchEngineStruct when top results are empty.

    This test checks if the get_top_result method correctly returns an empty list when no search
    has been performed yet.
    """
    se = SearchEngineStruct()
    assert len(SearchEngineStruct.get_top_result(se)) == 0


def test_set_and_get_query():
    """
    Test the set_query and get_query methods of SearchEngineStruct.

    This test checks if a query string can be successfully set and retrieved using the
    set_query and get_query methods, respectively.
    """
    se = SearchEngineStruct()
    seed_query = "test_query"
    se.set_query(seed_query)
    assert se.get_query() == seed_query


def test_search_current_query_google_success():
    """
    Test the call_google_custom_search_api method of SearchEngineStruct with a valid query.

    This test checks if the call_google_custom_search_api method correctly updates the top_result
    attribute with at least 10 search results when provided with a valid query.
    """
    se = SearchEngineStruct()
    seed_query = "per se"
    se.set_query(seed_query)
    se.call_google_custom_search_api()
    assert len(se.get_top_result()) >= 10


def test_search_current_query_google_fail():
    """
    Test the call_google_custom_search_api method of SearchEngineStruct with an invalid query.

    This test checks if the call_google_custom_search_api method correctly raises a SearchException
    when provided with a query that results in less than 10 search results.
    """
    se = SearchEngineStruct()
    seed_query = "jjj sedskdsksdkdskdskdskdkssdkds"
    se.set_query(seed_query)
    with pytest.raises(SearchException):
        se.call_google_custom_search_api()


def test_choose_relevant_1(monkeypatch):
    """
    Test the choose_relevant method of SearchEngineStruct when all search results are relevant.

    This test checks if the choose_relevant method correctly updates the relevant and irrelevant
    attributes and returns an accuracy of 1 when all search results are considered relevant by the user.

    Args:
        monkeypatch: A fixture provided by pytest for mocking.
    """
    number_inputs = StringIO("Y\n" * 10)
    se = SearchEngineStruct()
    seed_query = "per se"
    se.set_query(seed_query)
    se.call_google_custom_search_api()
    monkeypatch.setattr("sys.stdin", number_inputs)
    assert se.choose_relevant() == 1
    assert len(se.relevant) == 10
    assert len(se.irrelevant) == 0


def test_choose_relevant_0(monkeypatch):
    """
    Test the choose_relevant method of SearchEngineStruct when no search results are relevant.

    This test checks if the choose_relevant method correctly updates the relevant and irrelevant
    attributes and returns an accuracy of 0 when no search results are considered relevant by the user.

    Args:
        monkeypatch: A fixture provided by pytest for mocking.
    """
    number_inputs = StringIO("N\n" * 10)
    se = SearchEngineStruct()
    seed_query = "per se"
    se.set_query(seed_query)
    se.call_google_custom_search_api()
    monkeypatch.setattr("sys.stdin", number_inputs)
    assert se.choose_relevant() == 0
    assert len(se.relevant) == 0
    assert len(se.irrelevant) == 10
