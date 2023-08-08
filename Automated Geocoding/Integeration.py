import requests
import json
"""
This Python script perform geocoding on Raw News data which is in our news aggregation database and save the processed geocoded data while removing the processed items from the non-geocoded dataset. The script utilizes the requests library for making HTTP requests to the specified APIs.
"""
# Step 1: Retrieve non-geocoded data from an API and save it to a file
"""
Step 1:
Open a file named "notgeocoded.json" in write mode.

Send an HTTP GET request to the non_geocoded_url API endpoint to retrieve non-geocoded data.

Write the response (data) obtained from the API into the "notgeocoded.json" file.

Close the file.
"""
files = open(r'notgeocoded.json', 'w')
non_geocoded_url = "https://i52oo81418.execute-api.us-east-1.amazonaws.com/production/notgeocoded"
response = requests.request("GET", non_geocoded_url)
res = response.text
print(res, file=files)
files.close()

# API's for geocoding process
get_raw_data_url = "https://i52oo81418.execute-api.us-east-1.amazonaws.com/production/geocoded"
geocoding_data_url = "https://trfmodel.coi6htut061eo.ap-south-1.cs.amazonlightsail.com/geocoder"
geocoded_data_post_url = "https://i52oo81418.execute-api.us-east-1.amazonaws.com/production/geocoded"
delete_geocoded_id_url = "https://i52oo81418.execute-api.us-east-1.amazonaws.com/production/notgeocoded"

headers = {'Content-Type': 'application/json'}

# Step 2: Process the geocoding for each item in the data_dict
with open('notgeocoded.json') as file:
    # Open a file named "1.json" containing a JSON object (data_dict).
    data_dict = json.load(file)
    count = 0
    for attr in data_dict:
        # Iterate through each item (attr) in the data_dict.
        count += 1

        # Step 2.1: Retrieve additional data for geocoding using RawData_objectID
        RawData_objectId = attr["RawData_ObjectID"]
        # Extract the "RawData_ObjectID" from the current item.

        payload1 = {'RawData_ObjectID': RawData_objectId}

        # Send an HTTP GET request to the get_raw_data_url API endpoint with the extracted "RawData_ObjectID" as a parameter to retrieve additional data for geocoding like news and headlines or complete document news.
        response1 = requests.request("GET", get_raw_data_url, params=payload1)
        res1 = response1.text
        res1 = json.loads(res1)
        temp = ''
        if (res1['subnews'] is not None):
            temp += res1['subnews']
        if (res1['article'] is not None):
            temp += res1['article']
        if (res1['summary'] is not None):
            temp += res1['summary']

        # Step 2.2: Send data for geocoding and receive the results
        payload2 = json.dumps({"key": temp})

        # Send an HTTP POST request to the geocoding_data_url API endpoint with the "temp" data as a JSON payload to perform geocoding using our model with flask web based backend API with spacy model.
        response2 = requests.request(
            "POST", geocoding_data_url, headers=headers, data=payload2)
        res2 = response2.text
        resans = json.loads(res2)
        resp = resans.replace("'", '"')
        geocoded_var = json.loads(resp)
        # Process the geocoding response (res2) and convert it into a JSON object (geocoded_var).
        print(geocoded_var)

        # Step 2.3: Process the geocoded data and prepare for returning
        array = []
        if (len(resp) > 5):
            # If the geocoded data is not empty, prepare an array (array) of geocoded data for each entry in the response.
            for itr in geocoded_var:
                payload3 = {
                    'Rawdata_ObjectId': RawData_objectId,
                    'geometry': {
                        'type': "Point",
                        'coordinates': [
                            float(geocoded_var[itr]['longitude']),
                            float(geocoded_var[itr]['latitude'])
                        ]
                    },
                    'property': {
                        'name': itr
                    }
                }
                array.append(payload3)
        json_data = json.dumps(array)

        # Step 2.4: Save the processed geocoded data in our database.
        # Send an HTTP POST request to the geocoded_data_post_url API endpoint with the processed geocoded data to save it.
        response3 = requests.request(
            "POST", geocoded_data_post_url, headers=headers, data=json_data)
        print(response3.text)

        # Step 2.5: Delete the processed item from non-geocoded data.

        # Send an HTTP DELETE request to the delete_geocoded_id_url API endpoint with the "_id" of the processed item as a JSON payload to remove it from the non-geocoded dataset.
        payload4 = json.dumps({"_id": attr["_id"]["$oid"]})
        response4 = requests.request(
            "DELETE", delete_geocoded_id_url, headers=headers, data=payload4)
        print(response4.text)

    # Step 3: Print the total number of items processed
    print(count)
