from flask import request, jsonify
from core import app
from flask_api import status
from repository.users import create_user,login_user,create_access_token, update_profile, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/',methods=['GET'])
def home_api():
    return {"name":"Client API", "status":"healthy"}, status.HTTP_200_OK

@app.route('/users.update',methods=['PUT'])
@jwt_required()
def updateUser():
    email = get_jwt_identity()
    return update_profile(request,email)

@app.route('/users.create',methods=['POST'])
def creatUser():
    return create_user(request)

@app.route('/users.login',methods=['POST'])
def loginUser():
    return login_user(request)

@app.route('/token/refresh')
@jwt_required(refresh=True)
def refreshToken():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return jsonify(access_token=access_token,refresh_token=refresh_token),status.HTTP_200_OK
    
