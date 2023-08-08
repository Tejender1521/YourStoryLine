from flask import request
from core import app
from repository.geocoded import get_news


@app.route('/get.news',methods=['GET'])
def getnews():
    return get_news(request)