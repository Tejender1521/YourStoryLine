from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv
import os

load_dotenv()

es = Elasticsearch(os.getenv("Elasticsearch_URL"))

resp = es.search(index="jaipur_index", query={"match": {"name": "Bhagwandas"}})
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    print("%(name)s %(latitude)s: %(longitude)s" % hit["_source"])