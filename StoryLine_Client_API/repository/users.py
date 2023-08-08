from flask_api import status
from db import get_db
from models.users import users
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import (create_access_token,
create_refresh_token)
from flask import jsonify


def create_user(request):
    db=get_db()
    newUser = request.get_json()
    signupUser = db.users.find_one({'email':newUser['email']})
    if signupUser:
        return jsonify(message='Email is already taken'),status.HTTP_400_BAD_REQUEST
    signupUser = db.users.find_one({'username':newUser['username']})
    if signupUser:
        return jsonify(message='Username is already taken'),status.HTTP_400_BAD_REQUEST
    newUser['password']=generate_password_hash(newUser['password'])
    temp = users()
    temp.create(newUser)
    access_token = create_access_token(identity=newUser['email'])
    refresh_token = create_refresh_token(identity=newUser['email'])
    return jsonify(access_token=access_token, refresh_token=refresh_token), status.HTTP_200_OK


def login_user(request):
    db=get_db()
    newUser = request.get_json()
    signupUser = db.users.find_one({'email':newUser['email']})
    if not signupUser:
        return jsonify(message='User does not exists'), status.HTTP_400_BAD_REQUEST
    if check_password_hash(signupUser['password'],generate_password_hash(newUser['password'])):
        return {'message':'Incorrect Password'},status.HTTP_400_BAD_REQUEST
    access_token = create_access_token(identity=newUser['email'])
    refresh_token = create_refresh_token(identity=newUser['email'])
    return jsonify(access_token=access_token, refresh_token=refresh_token), status.HTTP_200_OK

def update_profile(request,email):
    db=get_db()
    temp = users()
    error = temp.validator(request.get_json())
    userData = request.get_json()
    userData["_id"] = db.users.find_one({'email':email})["_id"]
    if error is None:
        object_id = temp.update(tem=userData)
        return object_id, status.HTTP_200_OK 
    else:
        return "INVALID DOCUMENT SCHEMA", status.HTTP_400_BAD_REQUEST

