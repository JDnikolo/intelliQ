from flask import request, Blueprint, jsonify
from mysqlconfig import myconnector
from authentication import authUser
from csvResponse import generateCSVresponse

getquestionanswers_blueprint = Blueprint("getquestionanswers", __name__)

@getquestionanswers_blueprint.route('/getquestionanswers/<questionnaireID>/<questionID>', methods = ['POST', 'GET'])
def getquestionanswers(questionnaireID,questionID):
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
                            "instance": "/Users/getquestionanswers"}), 400
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
                            "instance": "/Users/getquestionanswers"}), 400
                elif (args.get("format") == "json"):
                    format = "json"
                elif (args.get("format") == "csv"):
                    format = "csv"
                else:
                    return jsonify({"type": "/errors/operation-error",
                            "title": "Invalid format type.",
                            "status": "400",
                            "detail": "Only json and csv are acceptable formats.",
                            "instance": "/Users/getquestionanswers"}), 400
            sqlcursor = myconnector.cursor()
            sqlcursor.execute(''' SELECT sessionID, IF (STRCMP(`optionTXT`,"<open string>") != 0,
            ans_optionID, answertxt)
            FROM Answer INNER JOIN Qoption
            WHERE (optionID = ans_optionID AND questionID = %s AND qnrID = %s)
            ORDER BY answerID''',(str(questionID),str(questionnaireID)))
            #Order by answerID because it is chronologically given, thus 1st answer corresponds to 1st session
            result = sqlcursor.fetchall()
            if len(result) == 0:
                #ERROR TYPE????????????????????????????
                return jsonify({"type": "/errors/operation-error",
                            "title": "No answers found.",
                            "status": "402",
                            "detail": "No answers were found.",
                            "instance": "/Users/getquestionanswers"}), 402
            sqlcursor.close()
            for i in range(len(result)):
                result[i] = dict(session = result[i][0], ans = result[i][1])
            if (format == 'json'):
                return jsonify({"questionnaireID": str(questionnaireID),
                "questionID": str(questionID), "answers": result}), 200
            else:
                newDict = dict(questionnaireID = str(questionnaireID),
                session = str(questionID), answers = result)
                return generateCSVresponse(newDict, "answers")
        else:
            return jsonify({
                        "type":"/errors/authentication-error",
                        "title": "Unauthorized User",
                        "status": "401",
                        "detail":"User is unauthorized",
                        "instance":"/Users/getquestionanswers"}), 401

    if request.method == 'POST':
        #return jsonify({"status":"failed", "reason":"POST is invalid in getquestionanswers"}), 400
        #ERROR TYPE????????????????????????????
        return jsonify({"type": "/errors/operation-error",
                        "title": "Invalid method.",
                        "status": "405",
                        "detail": "POST is invalid in getsessionanswers.",
                        "instance": "/Users/getquestionanswers"}), 405
