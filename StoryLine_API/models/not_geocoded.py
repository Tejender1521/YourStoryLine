from db import db
from jsonschema import validate


class not_geocoded(object):

    def __init__(self):
        self.db=db()
        self.collection_name = 'not_geocoded'

        self.fields = {
            "RawData_ObjectID":"String",
        }
    
    def validator(self,element):
        schema = {
            "type": "object",
            "properties": {
                "RawData_ObjectID": {"type" : "string"},  
            },
            "required":["RawData_ObjectID"],
        }
        try:
            validate(instance=element, schema=schema)
        except:
            return "error"

    def create(self, tem):
        res = self.db.insert(tem, self.collection_name)
        return "Inserted Document ID: " + res
    
    def delete(self, tem):
        res = self.db.delete(tem, self.collection_name)
        return res
