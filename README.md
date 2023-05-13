# PyTorch-NLP-chatbot
NLP and its uses in creating an intelligent responsive chatbot to interact with users.

![Apache Liscence](https://img.shields.io/github/license/KoroIsCoding/PyTorch-NLP-chatbot)![Issue](https://img.shields.io/github/issues/KoroIsCoding/PyTorch-NLP-chatbot)

[![Build Status](https://github.com/KoroIsCoding/PyTorch-NLP-chatbot/actions/workflows/build.yml/badge.svg)](https://github.com/KoroIsCoding/PyTorch-NLP-chatbot/actions/workflows/build.yml)

[![PyPI](https://img.shields.io/pypi/v/PyTorch-NLP-Chatbot)](https://pypi.org/project/Pytorch-nlp-Chatbot/)


[![codecov](https://codecov.io/gh/KoroIsCoding/PyTorch-NLP-chatbot/branch/main/graph/badge.svg?token=Y6UI9PLM4A)](https://codecov.io/gh/KoroIsCoding/PyTorch-NLP-chatbot)


[![Docs](https://github.com/KoroIsCoding/PyTorch-NLP-chatbot/actions/workflows/documentation.yaml/badge.svg)](https://koroiscoding.github.io/PyTorch-NLP-chatbot/)

## Overview
`Python-Search-Engine` is a Python library designed to facilitate custom searches using the Google Search API. It features a user-friendly interface for querying, parsing, and analyzing search results. It also provides a mechanism to rank search results based on their relevance, calculated using TF-IDF scores.

Users can tailor their search queries, evaluate the relevance of search results, and refine their queries based on relevance feedback.

## Python Search Engine Library

This Python library, developed by Koro_Is_Coding, allows users to build a custom search engine using the Google Search API. It is designed to be intuitive and easy to use, with a focus on flexibility and adaptability to a wide range of search tasks. This library is licensed under Apache v2.0.

### Prerequisites

Before you begin, ensure you have met the following requirements:

- You have a `Windows/Linux/Mac` machine running Python 3.6+.
- You have installed the `requests`, `string`, `operator`, `sklearn`, and `nltk` libraries.

### Installation

1. Clone this repository on your local machine:

```bash
git clone https://github.com/KoroIs_Coding/Python-Search-Engine
```

2. Navigate to the cloned repository:

```bash
cd Python-Search-Engine
```

3. Install the required dependencies:

```bash
pip install requests string operator sklearn nltk
```

### Using the Python Search Engine Library

The `SearchEngineStruct` class is the main class for the search engine. It requires a Google API key and a Google Engine key for initialization. 

Here's a simple usage example:

```python
from search_engine import SearchEngineStruct

# Initialize the search engine
search_engine = SearchEngineStruct(google_api_key='YOUR_API_KEY', google_engine_key='YOUR_ENGINE_KEY')

# Define your query
search_engine.set_query('Your search query')

# Call Google Custom Search API
search_engine.call_google_custom_search_api()

# Get top results
top_results = search_engine.get_top_result()
```

Please replace `'YOUR_API_KEY'` and `'YOUR_ENGINE_KEY'` with your actual Google API key and Google Engine key respectively.

### Contributing

If you want to contribute to this library, please check out the `CONTRIBUTING.md` file.

### License

This project uses the following license: [Apache v2.0](https://apache.org/licenses/LICENSE-2.0).