from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
import configparser,os
from flask import g

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))


class db(object):
    def __init__(self):
        # self.client = MongoClient(config['PROD']['DB_URI'])  # configure db url
        self.db = get_db()  # configure db name

    def insert(self, element, collection_name):
        element["created"] = datetime.today().replace(microsecond=0) #.strftime("%m-%d-%Y")
        element["updated"] = datetime.today().replace(microsecond=0)
        inserted = self.db[collection_name].insert_one(element)  # insert data to db
        return str(inserted.inserted_id)
    
    def update(self, element, collection_name):
        element["updated"] = datetime.today().replace(microsecond=0)
        element_id=ObjectId(element["_id"])
        element.pop('_id',None)
        updated=self.db[collection_name].update_one({"_id": element_id}, { "$set" : element})
        return str(element_id)

    def delete(self,element,collection_name):
        element_id=ObjectId(element['_id'])
        deleted=self.db[collection_name].delete_one({"_id":element_id})
        return "DELETED"

def get_db():
    if 'db' not in g:
        g.db=MongoClient(config['PROD']['DB_URI']).newsyog
    return g.db
