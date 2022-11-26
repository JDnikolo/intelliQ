from flask import Blueprint, jsonify
from mysqlconfig import *

questionnaireid=Blueprint("questionnaireid", __name__)

@questionnaireid.route("/questionnaire/<questionnaireID>", methods=["GET"])
# User endpoint for returning object with general data and 
# questions of questionnaire with <questionnaireID>, ordered by questionID
def questionnaireidf(questionnaireID):
    sqlcursor = myconnector.cursor()
    sqlcursor.execute('''SELECT title from questionnaire where questionnaireID =  %s''',str(questionnaireID))
    title = sqlcursor.fetchall()
    sqlcursor.execute('''SELECT word from keywords where questionnaireID =  %s''',str(questionnaireID))
    keywords = sqlcursor.fetchall()
    sqlcursor.execute('''SELECT questionID, qtext, required, qtype from question where (qnrID =  %s) ORDER BY questionID''',str(questionnaireID))
    questions = sqlcursor.fetchall()
    sqlcursor.close()
    return jsonify({"questionnaireID": str(questionnaireID),
        "questionnaireTitle": title, "keywords": keywords, "questions": questions})