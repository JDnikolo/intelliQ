from flask import request, Blueprint, jsonify, Response
import mysql.connector
from mysqlconfig import *
from authentication import authUser

getsessionanswers_blueprint = Blueprint("getsessionanswers", __name__)

@getsessionanswers_blueprint.route('/getsessionanswers/<questionnaireID>/<session>', methods = ['POST', 'GET'])
def getsessionanswers(questionnaireID,session):
    if request.method == 'GET':
        if authUser():
            args = request.args
            if (len(args) == 0):
                format = "json"
            elif (len(args) > 1):
                return jsonify({"type": "/errors/operation-error",
                            "title": "Invalid query parameters.",
                            "status": "400",
                            "detail": "Only format is acceptable query parameter.",
                            "instance": "/Users/getsessionanswers"}), 400
            elif (len(args) == 1):
                temp = args.to_dict()
                temp = temp.keys()
                temp = list(temp)
                temp = temp[0]
                if (temp != "format"):
                    return jsonify({"type": "/errors/operation-error",
                            "title": "Invalid query parameters.",
                            "status": "400",
                            "detail": "Only format is acceptable query parameter.",
                            "instance": "/Users/getsessionanswers"}), 400
                elif (args.get("format") == "json"):
                    format = "json"
                elif (args.get("format") == "csv"):
                    format = "csv"
                else:
                    return jsonify({"type": "/errors/operation-error",
                            "title": "Invalid format type.",
                            "status": "400",
                            "detail": "Only json and csv are acceptable formats.",
                            "instance": "/Users/getsessionanswers"}), 400
            sqlcursor = myconnector.cursor()
            sqlcursor.execute(''' SELECT questionID, IF (STRCMP(`optionTXT`,"<open string>") != 0,
            ans_optionID, answertxt)
            FROM Answer INNER JOIN qoption
            WHERE (optionID = ans_optionID AND sessionID = %s AND qnrID = %s)
            ORDER BY questionID''',(str(session),str(questionnaireID)))
            result = sqlcursor.fetchall()
            if len(result) == 0:
                #ERROR TYPE????????????????????????????
                return jsonify({"type": "/errors/operation-error",
                            "title": "No answers found.",
                            "status": "402",
                            "detail": "No answers were found.",
                            "instance": "/Users/getsessionanswers"}), 402
            sqlcursor.close()
            for i in range(len(result)):
                result[i] = dict(qID = result[i][0], ans = result[i][1])
            return jsonify({"questionnaireID": str(questionnaireID),
            "session": str(session), "answers": result}), 200
        else:
            return jsonify({
                        "type":"/errors/authentication-error",
                        "title": "Unauthorized User",
                        "status": "401",
                        "detail":"User is unauthorized",
                        "instance":"/Users/getsessionanswers"}), 401

    if request.method == 'POST':
        #return jsonify({"status":"failed", "reason":"POST is invalid in getsessionanswers"}), 400
        #ERROR TYPE????????????????????????????
        return jsonify({"type": "/errors/operation-error",
                        "title": "Invalid method.",
                        "status": "405",
                        "detail": "POST is invalid in getsessionanswers.",
                        "instance": "/Users/getsessionanswers"}), 405
