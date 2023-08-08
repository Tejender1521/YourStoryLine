from flask_api import status
from db import get_db
from bson.json_util import dumps
from bson import ObjectId
from models.geocoded_data import geocoded


def get_rawdata(request):
    db=get_db()
    tem=request.args
    data=db.rawdata.find_one({"_id": ObjectId(tem["RawData_ObjectID"])})
    json_data=dumps(data,indent=4)
    return json_data


def insert_geocoded(request):
    temp = geocoded()
    data = request.get_json()
    if isinstance(data, list):
        # Iterate through the list and insert each element
        object_ids = []
        for element in data:
            error = temp.validator(element)
            if error is None:
                object_id = temp.create(tem=element)
                object_ids.append(object_id)
            else:
                return "INVALID DOCUMENT SCHEMA", status.HTTP_400_BAD_REQUEST
        return object_ids, status.HTTP_200_OK
    else:
        # Insert single element
        error = temp.validator(data)
        if error is None:
            object_id = temp.create(tem=data)
            return object_id, status.HTTP_200_OK
        else:
            return "INVALID DOCUMENT SCHEMA", status.HTTP_400_BAD_REQUEST
