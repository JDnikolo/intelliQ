from flask import request, Blueprint, jsonify
from mysqlconfig import myconnector

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
            return jsonify({
                "type":"/errors/not-found",
                "title": "Not Found",
                "status": "402",
                "detail":"No answers found.",
                "instance":"/getquestionanswers/{}/{}".format(questionnaireID, questionID)}), 402 #404
        sqlcursor.close()
        for i in range(len(result)):
            result[i] = dict(session = result[i][0], ans = result[i][1])
        return jsonify({"questionnaireID": str(questionnaireID),
        "questionID": str(questionID), "answers": result}), 200

    if request.method == 'POST':
        return jsonify({
                        "type":"/errors/method-not-allowed",
                        "title": "Method Not Allowed",
                        "status": "400",
                        "detail":"POST Request not allowed.",
                        "instance":"/getquestionanswers/{}/{}".format(questionnaireID, questionID)}), 400    #405