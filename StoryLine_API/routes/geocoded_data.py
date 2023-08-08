from flask import request
from core import app
from flask_api import status
from repository.geocoded_data import get_rawdata, insert_geocoded

@app.route('/',methods=['GET'])
def home():
    return {'status':'Healthy',"API Name":"Geocoding"}, status.HTTP_200_OK

@app.route('/geocoded',methods=['GET','POST'])
def query_g():
    if request.method=='GET':
        return get_rawdata(request), status.HTTP_200_OK
    if request.method=='POST':
        return insert_geocoded(request)
