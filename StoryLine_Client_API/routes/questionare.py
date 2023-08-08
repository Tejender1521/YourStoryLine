from flask import request
from core import app
from repository.questionare import add_question, get_question, del_question, mod_question

@app.route('/questionare',methods=['GET','POST','DELETE','PUT'])
def query_q():
    if request.method=='GET':
        return get_question(request)
    if request.method=='POST':
        return add_question(request)
    if request.method == 'PUT':
        return mod_question(request)
    if request.method=='DELETE':
        return del_question(request)


    