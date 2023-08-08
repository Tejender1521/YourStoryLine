from flask import Flask
import configparser,os
from datetime import timedelta
from flask_jwt_extended import JWTManager


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MONGO_URI'] = config['PROD']['DB_URI']
app.config["JWT_SECRET_KEY"] = "btkXMrsNpy"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
# app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
jwt = JWTManager(app)

from routes import users, questionare, geocoded