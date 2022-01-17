# semantically

## Introduction

Semantically is a Python library designed to easily retrieve data from Semantic Scholar. All data is typed in dataclasses built around the Semantic Scholar API. Furthermore semantically supports methods to retrieve papers by their title in order.
For larger requests semantically offers methods to retrieve papers according to lists of keywords. In the background these requests are run asynchronously so that several requests can be sent in a short amount of time.

## Requirements

Python 3.6+

Semantically relies mainly on

* Levenshtein
* dacite
* aiohttp

## Installation

Semantically can be installed via pip with

```
pip install 
```

## Examples

Using semantically to retrieve paper information is as easy as

```python
import semantically

semantic_scholar = semantically.Semantically()
paper_info = semantic_scholar.get_paper_by_title(
    "Supporting the Exploration of Semantic Features in Academic Literature using Graph-based Visualizations"
)

print(paper_info) # Paper(paperId='175ac9646f3a7b6491c6bad896c47c495633d54a', externalIds={'MAG': '3046741163', 'DBLP': 'conf/jcdl/BreitingerKMMG20', ...
```

Getting an author by name:

```python
import semantically

semantic_scholar = semantically.Semantically()
author_info = semantic_scholar.get_author_by_name("Albert Einstein")

print(author_info[0])  # DetailedAuthor(authorId='2059041927', externalIds={}, url='https://www.semanticscholar.org/author/2059041927',...
```

This example queries the API for 7 keywords, each containing 10 results:

```python
import semantically

keywords = ["Recommender System", "Blockchain", "Natural Language Processing", "Plagiarism Detection", "News Analysis", "Information Retrieval", "Machine Learning"]

semantic_scholar = semantically.Semantically()
paper_info = semantic_scholar.get_papers_by_keyword(keywords, limit=10)

print(paper_info["Natural Language Processing"][4]) # Paper(paperId='084c55d6432265785e3ff86a2e900a49d501c00a', externalIds=None, url=None, title='Foundations of statistical natural language processing'
```