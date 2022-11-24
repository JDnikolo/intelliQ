from flask import request, Blueprint, jsonify, Response
import mysql.connector
from mysqlconfig import *

getsessionanswers_blueprint = Blueprint("getsessionanswers", __name__)

@getsessionanswers_blueprint.route('/getsessionanswers/<questionnaireID>/<session>', methods = ['POST', 'GET'])
def getsessionanswers(questionnaireID,session):
    if request.method == 'GET':
        sqlcursor = myconnector.cursor()
        sqlcursor.execute(''' SELECT questionID, answerID FROM Answer INNER JOIN qoption
        WHERE (sessionID = %s AND qnrID = %s)
        ORDER BY questionID''',(str(session),str(questionnaireID)))
        result = sqlcursor.fetchall()
        if len(result) == 0:
            return Response("No answers found",status=402)
        sqlcursor.close()
        return jsonify({"questionnaireID": str(questionnaireID),
        "session": str(session), "answers": result}), 200
        
    if request.method == 'POST':
        return jsonify({"status":"failed", "reason":"POST is invalid in getsessionanswers"}), 400
