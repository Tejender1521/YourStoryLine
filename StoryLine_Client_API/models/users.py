from db import db
from jsonschema import validate


class users(object):

    def __init__(self):
        self.db=db()
        self.collection_name = 'users'

        self.fields = {
            "name": "string",
            "e-mail": "string",
            "username": "string",
            "password": "string",
            "interest": list,
            "subscriptions": list,
            "ques_ans": dict
        }
    
    def validator(self,element):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type" : "string"},  
                "username": {"type" : "string"},  
                "password": {"type" : "string"},  
            },
            "required":[],
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

    
