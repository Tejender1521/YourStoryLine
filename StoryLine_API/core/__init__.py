
from flask import Flask
import configparser,os


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MONGO_URI'] = config['PROD']['DB_URI']

from routes import geocoded_data, not_geocoded