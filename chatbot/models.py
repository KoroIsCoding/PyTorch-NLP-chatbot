# Authors: Koro_Is_Coding
# License: Apache v2.0
# Version: v.0.0.1

import requests
from string import Template
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import operator


class SearchException(Exception):
    """
    Exception raised when there are not enough search results.

    This exception is typically raised when the number of items in a search response is less than 10.

    Attributes:
        message -- explanation of the error
    """

    print("no enough results")


def cal_tfidf(results):
    """
    Calculate the TF-IDF scores for the words in the given search results.

    Each search result should be a dictionary with the keys "title" and "snippet".
    The words in these fields will be tokenized and used to calculate the TF-IDF scores.

    Args:
        results (list): A list of search result dictionaries. Each dictionary must have 'title'
                        and 'snippet' keys.

    Returns:
        dict: A dictionary mapping each word to its TF-IDF score.

    Raises:
        ValueError: If any of the dictionaries in the results list does not contain 'title'
                    or 'snippet' as keys.
    """
    words = []
    for result in results:
        words.extend(re.sub("[^\w]", " ", result["title"]).split())
        words.extend(re.sub("[^\w]", " ", result["snippet"]).split())

    tv = TfidfVectorizer()
    tv.fit_transform(words)
    return dict(zip(tv.get_feature_names_out(), tv.idf_))


class SearchEngineStruct:
    def __init__(
        self,
        google_api_key="AIzaSyAGHYwrgMmAHlFwM-GmS2anQ7xWu7qcIjA",
        google_engine_key="7a8bd65adc0b760d8",
    ):
        """
        Initialize the SearchEngineStruct with the given API keys.

        Args:
            google_api_key (str): The API key to use for Google's API. Default is an example key.
            google_engine_key (str): The engine key to use for Google's API. Default is an example key.

        Returns:
            None
        """
        self.google_api_key = google_api_key
        self.google_engine_key = google_engine_key
        self.top_result = list()
        self.relevant = list()
        self.irrelevant = list()
        self.query = ""

    def get_top_result(self):
        """
        Returns a copy of the top search results.

        This function does not modify the state of the SearchEngineStruct object.

        Args:
        None

        Returns:
            list: A copy of the list of the top search results.
        """
        return list(self.top_result)

    def set_query(self, seed_query):
        """
        Sets the query of the SearchEngineStruct object.

        This function modifies the state of the SearchEngineStruct object by updating the query.

        rgs:
            seed_query (str): The new query string.

        Returns:
            None
        """
        self.query = seed_query

    def get_query(self):
        """
        Returns the current query of the SearchEngineStruct object.

        This function does not modify the state of the SearchEngineStruct object.

        Args:
            None

        Returns:
            str: The current query string.
        """
        return self.query

    def call_google_custom_search_api(self):
        """
        Call the Google Custom Search API with the current query.

        This function updates the top_result attribute with the results returned by the API.

        Args:
            None

        Returns:
            None

        Raises:
            SearchException: If the API response is None, or if there are less than 10 items in the response.
        """
        URL = Template("https://www.googleapis.com/customsearch/v1?key=$client_key&cx=$engine_key&q=$query")
        url = URL.substitute(
            client_key=self.google_api_key,
            engine_key=self.google_engine_key,
            query=self.query,
        )
        response = requests.get(url)
        if response is None:
            raise SearchException
        else:
            try:
                if len(response.json()["items"]) < 10:
                    raise SearchException
                else:
                    self.top_result = response.json()["items"]
            except KeyError:
                raise SearchException

    def choose_relevant(self):
        """
        This function takes a list of search results and iteratively displays each result to the user
        and asks if it is relevant or not. The user input is used to split the search results into two
        separate lists: relevant and irrelevant.

        Args:
        - results (list of dict): a list of search results returned by the search engine. Each search
          result is a dictionary with the following keys: "link", "title", and "snippet".

        Returns:
        - accuracy (float): the percentage of relevant search results out of the total number of
          search results (i.e., the number of search results in the input list).
        """
        results = self.top_result
        count = 0

        for i in range(len(results)):
            result = results[i]
            print("Result %d" % (i + 1))
            print("[")
            print(" URL: " + result["link"])
            print(" Title: " + result["title"])
            print(" Summary: " + result["snippet"])
            print("]")
            ans = input("Relevant (Y/N)?")

            if ans.upper() == "Y":
                count += 1
                self.relevant.append(result)
                print("RELEVANT")
            else:
                self.irrelevant.append(result)
                print("NOT RELEVANT")
        accuracy = count / float(10)
        return accuracy

    def add_and_reorder_words(self):
        """
        Update the query based on the relevance feedback.

        This function calculates the TF-IDF scores for the words in the relevant and irrelevant results,
        finds the words that are unique to the relevant results, and adds the top two unique words to the query.
        This function has a side effect of updating the query attribute.

        Args:
            None

        Returns:
            None
        """
        query_old = self.query
        # Calculate TF-IDF scores for words in relevant and irrelevant results
        relevant_tfidf = cal_tfidf(self.relevant)
        irrelevant_tfidf = cal_tfidf(self.irrelevant)
        # Find words that are unique to relevant results
        unique_words = {key: value for key, value in relevant_tfidf.items() if key not in irrelevant_tfidf}
        # Sort unique words by their TF-IDF scores
        unique_words_sorted = sorted(unique_words.items(), key=operator.itemgetter(1))
        # Add the top two new words different from the original query
        count = 0
        modified_query = []
        words_old = query_old.split()
        for key in unique_words_sorted:
            if key[0] in words_old:
                modified_query.append(key[0])
                words_old.remove(key[0])
            elif count < 2 and key[0] not in query_old:
                modified_query.append(key[0])
                count += 1
        # Add the remaining words from the original query
        for word in words_old:
            modified_query.append(word)
            self.query = modified_query
