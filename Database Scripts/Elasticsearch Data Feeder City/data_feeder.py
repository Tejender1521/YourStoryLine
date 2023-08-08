# Import necessary modules
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import time
import json

# Create a connection to the Elasticsearch server
from dotenv import load_dotenv
import os

load_dotenv()

es = Elasticsearch(os.getenv("Elasticsearch_URL"))



def documents():
    """
    This function reads data from a JSON file ('new.json') and generates actions to index the data into Elasticsearch.

    Returns:
    actions (generator): A generator that yields individual actions to be indexed.

    """

    # Create an empty dictionary to store actions
    actions = {}

    # Open and load data from 'new.json' file
    with open('new.json') as file:
        data_dict = json.load(file)

        # Loop through the data in 'data_dict'
        for attr in data_dict:
            for place in data_dict[attr]:
                try:
                    # Extract necessary data for indexing into Elasticsearch
                    doc = {
                        "name": place,
                        "latitude": data_dict[attr][place]['latitude'],
                        "longitude": data_dict[attr][place]['longitude']
                    }

                    # Create an action to index the document
                    action = {
                        "_index": "jaipur_index",
                        "_source": doc
                    }

                    # Yield the action for indexing
                    yield action
                except:
                    # If an exception occurs, skip the current iteration and continue with the next one
                    continue




if __name__ == "__main__":
    """
    It performs the following steps:
    1. Generate the actions to be indexed using the 'documents' function.
    2. Index the generated actions into Elasticsearch using 'helpers.bulk'.
    3. Refresh the index to make the changes available for search.
    """

    # Step 1: Generate actions to index data into Elasticsearch
    actions = documents()

    # Step 2: Bulk index the generated actions into Elasticsearch
    helpers.bulk(es, actions, chunk_size=500)

    # Step 3: Refresh the index to make the changes available for search
    es.indices.refresh(index='jaipur_index')
