from flask_api import status
from db import get_db


def get_news(request):
    data = request.args
    db=get_db()
    offset = int(data['pagenum']) * int(data['pagesize']) - int(data['pagesize'])
    filter={
    'geometry': {
        '$near': {
            '$maxDistance': int(data['radius']), 
            '$geometry': {
                'type': data['type'], 
                'coordinates': [
                    float(data['lat']), float(data['long'])
                ]
            }
        }
    }
    }
    listdata = list(db.geocoded.find(filter)    # filtering applied 
                                .sort("created",1) # sort by date
                                .skip( offset )  # skip the entries from previous page
                                .limit( int(data['pagesize']) )  # limit the entries of current page
                                )
    return listdata, status.HTTP_200_OK
