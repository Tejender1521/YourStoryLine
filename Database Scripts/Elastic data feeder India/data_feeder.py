# Import necessary libraries
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import csv
from tqdm import tqdm  # A progress bar library
"""
This code reads data from a CSV file IN.txt containing location information from Geonames.org from that data into an Elasticsearch index named "india_index." It uses the helpers.bulk method to efficiently index multiple documents at once, which helps in reducing the number of requests made to Elasticsearch or send data in bulk. The code also includes a progress bar using the tqdm library to show the progress while reading and indexing the data. If any errors occur during indexing, the code ignores them and continues processing the rest of the data.
"""
# Connect to the Elasticsearch cluster which is deployed on AWS Instance

from dotenv import load_dotenv
import os

load_dotenv()

es = Elasticsearch(os.getenv("Elasticsearch_URL"))
# Define the function to generate documents for indexing


def documents():
    actions = {}  # Initialize an empty dictionary to hold actions
    with open('IN.txt') as file:  # Open the 'IN.txt' CSV file
        # Read the data from IN.txt file and iterate
        reader = csv.reader(file, delimiter='\t')
        # Iterate through the CSV rows with a progress bar
        for row in tqdm(reader, total=649011):
            try:
                # Create a document to be indexed in Elasticsearch. This document create and converts the csv information to Geojson format.
                doc = {
                    "place_name": row[1],
                    "place_data": {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [row[5], row[4]]
                        },
                        "properties": {
                            "name": row[1],
                            "locality": row[1],
                            "country": "India",
                            "country_code": "IND",
                            "continent": "Asia",
                        }
                    }
                }
                action = {
                    "_index": "india_index",  # Specify the index name in Elasticsearch
                    "_source": doc  # Set the document to be indexed
                }
                yield action  # Yield the action to be executed later
            except:
                continue  # Skip rows with errors and continue with the next row
        return actions  # Return the actions dictionary


if __name__ == "__main__":
    # Call the 'documents' function to generate actions for indexing
    actions = documents()

    # Use the 'helpers.bulk' method to efficiently index documents in Elasticsearch
    helpers.bulk(es, actions, chunk_size=500)

    # Refresh the Elasticsearch index to make the new data available for search
    es.indices.refresh(index='india_index')
