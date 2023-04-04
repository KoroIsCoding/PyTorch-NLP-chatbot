# Authors: Koro_Is_Coding
# License: Apache v2.0

import sys
import requests
import re
import operator
from string import Template
from sklearn.feature_extraction.text import TfidfVectorizer

class SearchException(Exception):
    pass


class SearchEngineStruct:
    def __init__(self, google_api_key, google_engine_key):
        self.google_api_key = google_api_key
        self.google_engine_key = google_engine_key
        