from flask import request, Blueprint, jsonify, Response
import mysql.connector
from mysqlconfig import *

getsessionanswers_blueprint = Blueprint("getsessionanswers", __name__)

@getsessionanswers_blueprint.route('/getsessionanswers/<questionnaireID>/<session>', methods = ['POST', 'GET'])
def getsessionanswers(questionnaireID,session):
    if request.method == 'GET':
        sqlcursor = myconnector.cursor()
        sqlcursor.execute(''' SELECT questionID, IF (STRCMP(`optionTXT`,"<open string>") != 0,
        ans_optionID, answertxt)
        FROM Answer INNER JOIN qoption
        WHERE (optionID = ans_optionID AND sessionID = %s AND qnrID = %s)
        ORDER BY questionID''',(str(session),str(questionnaireID)))
        result = sqlcursor.fetchall()
        if len(result) == 0:
            return Response("No answers found",status=402)
        sqlcursor.close()
        for i in range(len(result)):
            result[i] = dict(qID = result[i][0], ans = result[i][1])
        return jsonify({"questionnaireID": str(questionnaireID),
        "session": str(session), "answers": result}), 200
        
    if request.method == 'POST':
        return jsonify({"status":"failed", "reason":"POST is invalid in getsessionanswers"}), 400
