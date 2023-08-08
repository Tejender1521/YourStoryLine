from flask_api import status
from db import get_db
from bson.json_util import dumps
from models.not_geocoded import not_geocoded


def get_non_geocoded(request):
    db = get_db()
    tem = request.args
    list_data = list(db.not_geocoded.find().limit(
            int(tem["Count"])).sort([('_id', -1)]))
    json_data = dumps(list_data, indent=4)
    return json_data

        



def insert_notgeocoded(request):
    temp = not_geocoded()
    error = temp.validator(request.get_json())
    if error is None:
        object_id = temp.create(tem=request.get_json())
        return object_id, status.HTTP_200_OK
    else:
        return "INVALID DOCUMENT SCHEMA", status.HTTP_400_BAD_REQUEST


def delete_notgeocoded(request):
    temp = not_geocoded()
    result = temp.delete(tem=request.get_json())
    return result
