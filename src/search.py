import sys
import requests
import re
import operator
from string import Template
from sklearn.feature_extraction.text import TfidfVectorizer

URL = Template("https://www.googleapis.com/customsearch/v1?key=$client_key&cx=$engine_key&q=$query")
stop_words = []
irrelevant = []
relevant = []


def call_google_custom_search_api(url):
    response = requests.get(url)
    items = response.json()["items"]
    return items


def choose_relevant(results):
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
            relevant.append(result)
            print("RELEVANT")
        else:
            irrelevant.append(result)
            print("NOT RELEVANT")
    accuracy = count / float(10)
    return accuracy


def cal_tfidf(results):
    """
       Calculate the term frequency-inverse document frequency (TF-IDF) score for each word in a list of search results.

       Args:
           results (list): A list of dictionaries, where each dictionary represents a search result and has "title" and
           "snippet" keys.

       Returns:
           dict: A dictionary where each key is a word from the search results, and each value is its corresponding IDF
           score as calculated by the TF-IDF vectorizer.
       """

    words = []
    for result in results:
        words.extend(re.sub("[^\w]", " ", result["title"]).split())
        words.extend(re.sub("[^\w]", " ", result["snippet"]).split())

    tv = TfidfVectorizer(stop_words=stop_words)
    tv_fit = tv.fit_transform(words)
    return dict(zip(tv.get_feature_names_out(), tv.idf_))


def add_and_reorder_words(query_old):
    """
        Add and reorder words in a search query based on their relevance to the search results.

        Args:
            query_old (str): The original search query.

        relevant (list): A list of dictionaries containing relevant search results.
        irrelevant (list): A list of dictionaries containing irrelevant search results.

        Returns:
            list: A modified search query with the most relevant words first.
        """

    # Calculate TF-IDF scores for words in relevant and irrelevant results
    relevant_tfidf = cal_tfidf(relevant)
    irrelevant_tfidf = cal_tfidf(irrelevant)
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
    print("Augmenting by  " + ' '.join(modified_query))
    # Add the remaining words from the original query
    for word in words_old:
        modified_query.append(word)
    return modified_query


def main():
    if len(sys.argv) < 4: # check if there are enough arguments
        print("missiong arguments")
        return
    google_api_key = sys.argv[1]
    google_engine_key = sys.argv[2]
    precision = float(sys.argv[3])
    query = sys.argv[4].lower()

    f = open("stopword.txt", "r")
    global stop_words
    stop_words = f.read().split()
    f.close()
    while True:
        # Step 2
        url = URL.substitute(client_key=google_api_key, engine_key=google_engine_key, query=query)
        top_10_results = call_google_custom_search_api(url)
        if len(top_10_results) < 10:
            print("missing enough search results")
            return
        # Step 3
        print("Parameters:")
        print("Client key  = " + google_api_key)
        print("Engine key  = " + google_engine_key)
        print("Query       = " + query)
        print("Precision   = %.1f" % precision)
        print("Google Search Results:")
        print("======================")
        precision_10 = choose_relevant(top_10_results)
        # Step 4
        print("======================")
        print("FEEDBACK SUMMARY")
        print("Query " + query)
        print("Precision   = %.1f" % precision_10)
        if precision_10 >= precision or precision_10 == 0:
            print("Desired precision reached, done")
            break
        # precision not satisfied => continue
        print("Still below the desired precision of %.1f" % precision)
        print("Indexing results ....")
        print("Indexing results ....")
        # Step 5
        modified_query = add_and_reorder_words(query)
        # Go to Step 2 with the modified query
        query = ' '.join(modified_query)


if __name__ == "__main__":
    main()
