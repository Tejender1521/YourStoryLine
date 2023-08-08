from flask import request
from core import app
from flask_api import status
from repository.not_geocoded import get_non_geocoded, delete_notgeocoded, insert_notgeocoded


@app.route('/notgeocoded',methods=['GET','POST','DELETE'])
def query_ng():
    if request.method=='GET':
        return get_non_geocoded(request), status.HTTP_200_OK
    if request.method=='POST':
        return insert_notgeocoded(request)
    if request.method=='DELETE':
        return delete_notgeocoded(request), status.HTTP_200_OK
