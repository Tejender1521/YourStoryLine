from flask_api import status
from db import get_db
from models.questionare import questionare
from bson.json_util import dumps
from bson import ObjectId


def get_question(request):
    db=get_db()
    tem=request.args
    if "_id" not in tem:
        listdata = list(db.questionare.find()) 
        jsondata = dumps(listdata, indent=2)
        return jsondata, status.HTTP_200_OK
    else:
        list_data=list(db.questionare.find({"_id":ObjectId(tem["QiD"])}))
        json_data=dumps(list_data,indent=2)
        return json_data, status.HTTP_200_OK

def add_question(request):
    data=request.get_json()
    temp= questionare()
    error=temp.validator(data)
    if error is None:
        object_id = temp.create(tem=data)
        return object_id, status.HTTP_200_OK 
    else:
        return "INVALID DOCUMENT SCHEMA", status.HTTP_400_BAD_REQUEST

def del_question(request):
    temp= questionare()
    return temp.delete(tem=request.get_json()), status.HTTP_200_OK

def mod_question(request):
    temp = questionare()
    return temp.update(tem=request.get_json()), status.HTTP_200_OK


