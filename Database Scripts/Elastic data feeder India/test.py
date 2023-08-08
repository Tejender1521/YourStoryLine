
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

es = Elasticsearch(os.getenv("Elasticsearch_URL"))


# define the index to search in
index_name = "india_index"

# define the search query
search_query = {
    "query": {
        "match_phrase": {
            "place_name": "Jaipur"
        }
    }
}

# execute the search query
search_results = es.search(index=index_name, body=search_query)

# print the results
for hit in search_results["hits"]["hits"]:
    print(hit["_source"])
