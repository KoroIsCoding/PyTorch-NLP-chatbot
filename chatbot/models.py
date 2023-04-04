# Authors: Koro_Is_Coding
# License: Apache v2.0

import sys
import requests
import re
import operator
from string import Template
from sklearn.feature_extraction.text import TfidfVectorizer


class SearchException(Exception):
    print("no enough results")


class SearchEngineStruct:
    def __init__(self, google_api_key='AIzaSyAGHYwrgMmAHlFwM-GmS2anQ7xWu7qcIjA', google_engine_key='7a8bd65adc0b760d8'):
        self.google_api_key = google_api_key
        self.google_engine_key = google_engine_key
        self.top_result = list()
        self.relevant = list()
        self.irrelevant = list()
        self.query = ''

    def get_top_result(self):
        return list(self.top_result)

    def set_query(self, seed_query):
        self.query = seed_query

    def get_query(self):
        return self.query

    def call_google_custom_search_api(self):
        URL = Template("https://www.googleapis.com/customsearch/v1?key=$client_key&cx=$engine_key&q=$query")
        url = URL.substitute(client_key=self.google_api_key, engine_key=self.google_engine_key, query=self.query)
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

    def kk(self):
        a = input("ssss")
        return a


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
