import json
from db import db
from jsonschema import validate


class geocoded(object):

    def __init__(self):
        self.db=db()
        self.collection_name = 'geocoded_data'

        self.fields = {
            "Rawdata_ObjectId":"String",
            "geometry": json,
            "property": json
        }
    
    def validator(self,element):
        schema = {
            "type": "object",
            "properties": {
                "Rawdata_ObjectId": {"type" : "string"},  
            },
            "required":["Rawdata_ObjectId", "geometry"],
        }
        try:
            validate(instance=element, schema=schema)
        except:
            return "error"

    def create(self, tem):
        res = self.db.insert(tem, self.collection_name)
        return "Inserted Document ID: " + res
    
