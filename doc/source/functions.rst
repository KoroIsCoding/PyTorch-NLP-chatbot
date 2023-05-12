Functions
=============

Available
*******************


* cal_tfidf(results) --> Returns a dictionary with words as keys and their corresponding TF-IDF scores as values
* SearchEngineStruct.__init__(self, google_api_key=default, google_engine_key=default) --> Initializes a SearchEngineStruct object with google API key, google engine key, top results list, relevant results list, irrelevant results list, and an empty query
* SearchEngineStruct.get_top_result(self) --> Returns a list of top results
* SearchEngineStruct.set_query(self, seed_query) --> Sets the search query
* SearchEngineStruct.get_query(self) --> Returns the current search query
* SearchEngineStruct.call_google_custom_search_api(self) --> Makes a call to Google's custom search API and sets top results. Raises a SearchException if there are less than 10 results or if the response is None
* SearchEngineStruct.choose_relevant(self) --> Iteratively displays each result to the user and asks if it is relevant or not. Splits the search results into two separate lists: relevant and irrelevant. Returns the percentage of relevant search results
* SearchEngineStruct.add_and_reorder_words(self) --> Modifies the search query by adding the top two new words (according to their TF-IDF scores) that are unique to the relevant results and are different from the original query. It maintains the remaining words from the original query. 


To Be Implemented
********************

* more NLP algorithm for query and document selection