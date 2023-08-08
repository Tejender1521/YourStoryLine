from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import json
"""
The script assumes that an Elasticsearch cluster is running and accessible at the specified URL (http://13.232.30.75:9200/).


If the cluster's location or configuration changes, the URL needs to be updated accordingly.


The script assumes that the file "sample.json" exists in the same directory as the script and contains valid GeoJSON data."""
from dotenv import load_dotenv
import os

load_dotenv()

es = Elasticsearch(os.getenv("Elasticsearch_URL"))


"""
This Python script interacts with an Elasticsearch instance deployed on AWS and loads data from a JSON file into the cluster's index named "global_index". The script reads data from a file named "sample.json" where scrapped data of position stack is there and iterates through its contents to create documents that are indexed in Elasticsearch in geojson format.
"""


def documents():
    actions = {}  # Initialize an empty dictionary
    count = 0  # Initialize a counter for exception occurrences

    with open('sample.json') as file:
        # Load JSON data from the file into a Python dictionary
        data_dict = json.load(file)

        for attr in data_dict:
            for place in data_dict[attr]:
                try:
                    doc = {
                        "place_name": attr,
                        "place_data": place
                    }
                    action = {
                        "_index": "global_index",
                        "_source": doc
                    }
                    yield action  # Return the action to be used in the bulk insert operation
                except:
                    count = count + 1
                    continue  # Skip to the next iteration in case of an exception


"""
It reads data from the JSON file and yields individual Elasticsearch action objects for each document.

Each document is represented as a Python dictionary with the fields "place_name" and "place_data".

The yield statement is used to produce a generator that allows the bulk insert operation to consume the actions one by one.

If an exception occurs during the processing of a document, it is caught, and the count variable is incremented. The script then continues to the next document.
"""

if __name__ == "__main__":
    actions = documents()  # Retrieve the generator of actions from the documents() function
    # Perform a bulk insert operation with a chunk size of 500
    helpers.bulk(es, actions, chunk_size=500)
    # Refresh the index "global_index" to make the changes visible
    es.indices.refresh(index='global_index')

"""
It retrieves the generator of actions from the documents() function and stores it in the actions variable.

The helpers.bulk() function is used to perform a bulk insert operation, taking advantage of the generator to efficiently process and insert multiple documents at once. 

The chunk_size parameter specifies the number of documents to be sent in each chunk during the bulk insert.

After inserting the documents, the script refreshes the Elasticsearch index "global_index" using es.indices.refresh() to ensure that the changes are visible for search and querying.
"""
