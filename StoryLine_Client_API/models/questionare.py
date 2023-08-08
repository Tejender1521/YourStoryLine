from db import db
from jsonschema import validate


class questionare(object):

    def __init__(self):
        self.db=db()
        self.collection_name = 'questionare'

        self.fields = {
            "question": "string",
            "answers": list
        }
    
    def validator(self,element):
        schema = {
            "type": "object",
            "properties": {
                "question": {"type" : "string"},  
                "answers": {"type" : list},  
            },
            "required":["question","answers"],
        }
        try:
            validate(instance=element, schema=schema)
        except:
            return "error"

    def create(self, tem):
        res = self.db.insert(tem, self.collection_name)
        return "Inserted Document ID: " + res
    
    def update(self, tem):
        res = self.db.update(tem, self.collection_name)
        return "Updated Document ID: " + res
    
    def delete(self, tem):
        res = self.db.delete(tem, self.collection_name)
        return res

    
