# Import required libraries
import json
from flask_cors import CORS, cross_origin
from flask import Flask, request
from elasticsearch import Elasticsearch
import spacy
from dotenv import load_dotenv
import os

load_dotenv()



"""
This code is a Flask web application that exposes two routes: a welcome page at the root ("/") and a geocoder endpoint ("/geocoder") that performs named entity recognition (NER) using spaCy and then performs geocoding using Elasticsearch based on the recognized named entities. The application listens on all available network interfaces on port 5000. The Elasticsearch URL is hard-coded to 'http://13.232.30.75:9200/', and two indexes ('india_index' and 'global_index') are searched for geocoding data. Please ensure that the Elasticsearch server is running and contains the required indexes for the application to work correctly.
"""


# Initialize the Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the app
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Load the spaCy model for named entity recognition (NER) in English
sp_sm = spacy.load('en_core_web_trf')


def spacy_large_ner(document):
    """
    Perform named entity recognition (NER) on the given document using the spaCy model.

    Parameters:
    document (str): The input text to process.

    Returns:
    set: A set of unique named entities recognized in the document, filtered for specific types (FAC, LOC, GPE).
    """
    a = set()
    for ent in sp_sm(document).ents:
        if (ent.label_ == "FAC" or ent.label_ == "LOC" or ent.label_ == "GPE"):
            a.add(ent.text.strip())
    return a


def esClosure():
    """
    Create and configure an Elasticsearch instance with the specified URL deployed on AWS.

    Returns:
    function: A function that returns the configured Elasticsearch instance as a context .
    """
    es = Elasticsearch(os.getenv("Elasticsearch_URL"))

    def esFunc():
        return es
    return esFunc


# Create an Elasticsearch context function and get the Elasticsearch instance
esContextFunc = esClosure()
esInstance = esContextFunc()


@app.route("/")
def welcome():
    """
    Welcome page for the service.

    Returns:
    str: A simple HTML response indicating that the service is running properly.
    """
    return "<p>Service is running properly.....</p>"


@app.post("/geocoder")
@cross_origin()
def hello_world():
    """
    Endpoint to perform geocoding using NER and Elasticsearch.

    Expects a JSON payload with a "key" field containing the text to geocode.

    Returns:
    flask.Response: A JSON response with geocoding results for recognized named entities.
    """
    data = request.get_json(force=True)
    text = data["key"]
    result = spacy_large_ner(text)
    print(result)
    newData = {}
    for word in result:
        """
        Search the keywords in indea_index on elasticsearch and then update the dictionary.
        """
        resp2 = esInstance.search(index="india_index", body={
                                  "query": {"match_phrase": {"place_name": word}}})
        for hit in resp2['hits']['hits']:
            place_data = "%(place_data)s" % hit["_source"]
            newData[word] = {"place_data": place_data}
            break

        if word in newData:
            continue
        """
        If keyword not found in india_index then search for global_index.


        Search the keywords in global_index on elasticsearch and then update the dictionary.
        """
        resp2 = esInstance.search(index="global_index", body={
                                  "query": {"match_phrase": {"place_name": word}}})
        for hit in resp2['hits']['hits']:
            place_data = "%(place_data)s" % hit["_source"]
            newData[word] = {"place_data": place_data}

    # Jsonify the data to send back to client
    newData = json.dumps(str(newData))

    response = app.response_class(
        response=newData,
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    # Run the Flask app on all available network interfaces on port 5000
    app.run(host='0.0.0.0', port=5000)
