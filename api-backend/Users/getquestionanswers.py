from flask import request, Blueprint, jsonify, Response
import mysql.connector
from mysqlconfig import *

getquestionanswers_blueprint = Blueprint("getquestionanswers", __name__)

@getquestionanswers_blueprint.route('/getquestionanswers/<questionnaireID>/<questionID>', methods = ['POST', 'GET'])
def getquestionanswers(questionnaireID,questionID):
    if request.method == 'GET':
        sqlcursor = myconnector.cursor()
        sqlcursor.execute(''' SELECT sessionID, IF (STRCMP(`optionTXT`,"<open string>") != 0,
        ans_optionID, answertxt)
        FROM Answer INNER JOIN qoption
        WHERE (optionID = ans_optionID AND questionID = %s AND qnrID = %s)
        ORDER BY sessionID''',(str(questionID),str(questionnaireID)))
        result = sqlcursor.fetchall()
        if len(result) == 0:
            return Response("No answers found",status=402)
        sqlcursor.close()
        for i in range(len(result)):
            result[i] = dict(session = result[i][0], ans = result[i][1])
        return jsonify({"questionnaireID": str(questionnaireID),
        "questionID": str(questionID), "answers": result}), 200

    if request.method == 'POST':
        return jsonify({"status":"failed", "reason":"POST is invalid in getquestionanswers"}), 400