from datetime import datetime
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

es = Elasticsearch(os.getenv("Elasticsearch_URL"))

res = es.search(index="mnit_03d962b2-4082-4ad2-a302-e2393808e982_geojson", body={
    "query": {
        "match_phrase": {
            "name": "Tagore Hospital and Research Institute"
        }
    }
})

for hit in res['hits']['hits']: 
    print(hit["_source"])
    # print("%(name)s  \n\n" % hit["_source"])
