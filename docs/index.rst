PyTorch-NLP-Chantbot Documentation!
================================================

Introduction
==================

Welcome to PyTorch-NLP-Chantbot's documentation. Here we explain how to setup the library, the functions available, and various examples.

About
==================

This project implement an information retrieval system that exploits user-provided relevance feedback to improve the search results returned 
by Google. The relevance feedback mechanism is described in Singhal: Modern Information Retrieval: A Brief Overview, IEEE Data Engineering Bulletin, 2001.
After choosing the feedback from the user, you can collect the result for further chatbot buildign system.

In essence, this project is a basic implementation of a relevance feedback system using Python and Google's Custom Search API, which allows users to improve 
the precision of their searches based on their feedback. This system can serve as a foundation for more complex, personalized search systems.


Installation
==================

#. clone from GitHub or **pip install PyTorch-NLP-Chantbot**
#. Install virtual environment: python -m venv env
#. Activate virtual env: source env/bin/activate
#. Install the dependencies: pip install .[develop]
#. python setup.py build
#. make lint
#. make test
#. Using the model's functions: chatbot/models.py

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   chatbot.rst
   functions.rst
   examples.rst
   modules.rst
   
