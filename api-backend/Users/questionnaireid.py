from flask import Blueprint, jsonify, Response
from mysqlconfig import *

questionnaireid=Blueprint("questionnaireid", __name__)

@questionnaireid.route("/questionnaire/<questionnaireID>", methods=["GET"])
# User endpoint for returning object with general data and 
# questions of questionnaire with <questionnaireID>, ordered by questionID
def questionnaireidf(questionnaireID):
    
    #if questionnaireID does not have QQxyz format, return bad request code
    if ((len(questionnaireID) != 5)):
        return Response("Required field was not given or is incorrectly formatted", status=400)
    
    sqlcursor = myconnector.cursor()
    sqlcursor.execute('''SELECT title from questionnaire where (questionnaireID =  %s)''',(str(questionnaireID),))
    title = sqlcursor.fetchall()
    
    #Check if given questionnaireID exists in database
    if len(title) == 0:
            return Response("The requested questionnaire is not present in the database", status=400) 
        
    sqlcursor.execute('''SELECT word from keywords where (questionnaireID =  %s)''',(str(questionnaireID),))
    keywords = sqlcursor.fetchall()
    sqlcursor.execute('''SELECT questionID as qID, qtext, required, qtype as type from question where (qnrID =  %s) ORDER BY questionID''',(str(questionnaireID),))
    questions = sqlcursor.fetchall()
    sqlcursor.close()
    
    return jsonify({"questionnaireID": (str(questionnaireID),),
        "questionnaireTitle": title, "keywords": keywords, "questions": questions}), 200