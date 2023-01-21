from flask import Blueprint, jsonify, request
from mysqlconfig import myconnector
from authentication import authUser
from csvResponse import generateCSVresponse

questionnaireid=Blueprint("questionnaireid", __name__)

@questionnaireid.route("/questionnaire/<questionnaireID>", methods=['POST', 'GET'])
# User endpoint for returning object with general data and 
# questions of questionnaire with <questionnaireID>, ordered by questionID
def questionnaireidf(questionnaireID):
    
    if request.method == "POST":
        return jsonify({
                        "type":"/errors/method-not-allowed",
                        "title": "Method Not Allowed",
                        "status": "400",
                        "detail":"POST Request not allowed.",
                        "instance":"/questionnaire/{}".format(questionnaireID)}), 400    #405
        
    if request.method == "GET":
        
        form = request.args.get("format", None)
        if form not in ['json', 'csv']:
            form = 'json'
            
        # Verify User
        if authUser():
        
            #if questionnaireID does not have QQxyz format, return bad request code
            if ((len(questionnaireID) != 5)):
                return jsonify({
                "type":"/errors/invalid-input",
                "title": "Bad Request",
                "status": "400",
                "detail":"Required field was not given or is incorrectly formatted.",
                "instance":"/questionnaire/{}".format(questionnaireID)}), 400
            
            sqlcursor = myconnector.cursor()
            sqlcursor.execute('''SELECT title from Questionnaire where (questionnaireID =  %s)''',(str(questionnaireID),))
            title = sqlcursor.fetchall()
            
            #Check if given questionnaireID exists in database
            if len(title) == 0:
                    return jsonify({
                "type":"/errors/not-found",
                "title": "Not Found",
                "status": "400",
                "detail":"The requested questionnaire is not present in the database.",
                "instance":"/questionnaire/{}".format(questionnaireID)}), 400    #404
                
            sqlcursor.execute('''SELECT word from Keywords where (questionnaireID =  %s)''',(str(questionnaireID),))
            keywords = sqlcursor.fetchall()
            sqlcursor.execute('''SELECT questionID as qID, qtext, required, qtype as type from Question where (qnrID =  %s) ORDER BY questionID''',(str(questionnaireID),))
            questions = sqlcursor.fetchall()
            sqlcursor.close()
            
            output = {"questionnaireID": (str(questionnaireID),),
                "questionnaireTitle": title, "keywords": keywords, "questions": questions}
            if form == 'json':
                return jsonify(output), 200
            if form == 'csv':
                return generateCSVresponse(output, listKey=None, filename="healthcheck.csv"), 200
            #return jsonify({"questionnaireID": (str(questionnaireID),),
                #"questionnaireTitle": title, "keywords": keywords, "questions": questions}), 200
        else:
            return jsonify({
                        "type":"/errors/authentication-error",
                        "title": "Unauthorized User",
                        "status": "401",
                        "detail":"User is unauthorized",
                        "instance":"/questionnaire/<questionnaireID>"}), 401 