import sys
import operator
import requests
import re

from string import Template
from sklearn.feature_extraction.text import TfidfVectorizer


# Google API query template
URL = Template("https://www.googleapis.com/customsearch/v1?key=$client_key&cx=$engine_key&q=$query")

NO_DOCS = []
YES_DOCS = []

def call_google_custom_search_api(url):
    response = requests.get(url)
    items = response.json()["items"]
    return items

def display_result(result):
    print("[")
    print(" URL: " + result["link"])
    print(" Title: " + result["title"])
    print(" Summary: " + result["snippet"])
    print("]")

def choose_relevant(results):
    count = 0
    for index in range(len(results)):
        print("Result %d" % (index + 1))
        display_result(results[index])

        # ask for feedback
        relevance = input("Relevant (Y/N)?")

        # record feedback
        if relevance.lower() == "y":
            count += 1
            YES_DOCS.append(results[index])
            print("RELEVANT")
        else:
            NO_DOCS.append(results[index])
            print("NOT RELEVANT")

    acc = count / float(10)
    print("Precision = %.1f" % acc)
    return acc

def get_words(docs):
    """Returns a list of words from the `title` and `snippet` sections, discounting punctuation"""
    words = []
    for doc in docs:
        words.extend(re.sub("[^\w]", " ", doc["title"]).split())
        words.extend(re.sub("[^\w]", " ", doc["snippet"]).split())
    return words


def tfidf(docs):
    """Return a dict of word: value pairs"""
    words = get_words(docs)
    vectorizer = TfidfVectorizer(stop_words=read_stopwords())
    x = vectorizer.fit_transform(words)
    idf = vectorizer.idf_
    return dict(zip(vectorizer.get_feature_names_out(), idf))


def ordered_tfidf_diff(yes, no):
    """Returns a sorted list of words that appear in the yes vector only"""
    unique_words = {}
    for key in yes:
        if key not in no:
            unique_words[key] = yes[key]
    return sorted(unique_words.items(), key=operator.itemgetter(1))


def read_stopwords():
    """Returns list of stopwords."""
    f = open("proj1-stop.txt", "r")
    words = f.read().split()
    f.close()
    return words

def add_and_reorder_words(query):
    # Get tf-idf values for our two sets of documents
    no_tfidf = tfidf(NO_DOCS)
    yes_tfidf = tfidf(YES_DOCS)
    diff = ordered_tfidf_diff(yes_tfidf, no_tfidf)

    # Create the new query: The old query plus two new words in descending order of calculated relevance
    new_query = []
    new_words = []
    old_words = query.split()
    for key in diff:
        if key[0] in old_words:
            new_query.append(key[0])
            old_words.remove(key[0])
        elif len(new_words) < 2 and query.find(key[0]) == -1:
            new_query.append(key[0])
            new_words.append(key[0])

    # append any of the old query words that didn't come up in the relevant documents (if any)
    for old_word in old_words:
        new_query.append(old_word)

    return new_query

def main():
    # check if there are enough arguments
    if len(sys.argv) < 4:
        print("missiong arguments")
        return

    # get the arguments
    google_api_key = sys.argv[1]
    google_engine_key = sys.argv[2]
    precision = float(sys.argv[3])
    query = sys.argv[4]


    while True:
        # Step 2
        url = URL.substitute(client_key=google_api_key, engine_key=google_engine_key, query=query)
        top_10_results = call_google_custom_search_api(url)

        # Step 3
        precision_10 = choose_relevant(top_10_results)

        # Step 4
        if precision_10 >= precision or precision_10 == 0:
            break

        # Step 5
        modified_query = add_and_reorder_words(query)

        # Go to Step 2 with the modified query
        query = modified_query

if __name__ == "__main__":
    main()