from mysqlconfig import *
from flask import jsonify, Blueprint, request
from authentication import authUser
from csvResponse import generateCSVresponse

question = Blueprint("question", __name__) 

@question.route("/question/<questionnaireID>/<questionID>", methods=["GET"])
def usr_question(questionnaireID: str, questionID: str):
    try:
        form = request.args.get("format", None)
        if form not in ['json', 'csv']:
            form = 'json'
        if authUser():
            sqlcursor = myconnector.cursor(buffered=True)
            #if qnrID doesnt have QQxyz format, or qID doesnt have Pxy format, return bad request code
            #if ((len(questionnaireID) != 5) or (len(questionID) != 3)):
            #    return Response("Required fields were not given or they are incorrectly formatted", status=400)
            #else check if they exist in the database.
            #SQL Query for checking
            sqlcursor.execute(
                '''SELECT Questionnaire.questionnaireID ,Question.questionID, Question.qtext,Question.required,Question.qtype
                   FROM (Questionnaire
                   INNER JOIN Question ON Questionnaire.questionnaireID = Question.qnrID)
                   WHERE (Questionnaire.questionnaireID = %s AND Question.questionID = %s)''',[questionnaireID, questionID])
            res = sqlcursor.fetchall()
            if len(res) == 0:
                return jsonify({
                        "type":"/errors/not-found",
                        "title": "Not Found",
                        "status": "400",
                        "detail":"The requested questionnaire/question is not present in the database.",
                        "instance":"/questionnaire/{}/{}".format(questionnaireID, questionID)}), 400    #404
            #save query data to return object
            for info in res:
                ret_data = {'questionnaireID' : info[0],
                            'qID' : info[1],
                            'qtext' : info[2],
                            'required' : str(info[3]),   #potentially need to convert 0/1 to false/true string here
                            'type' : info[4]}            
            #fetch options sorted by optID keys.
            sqlcursor.execute(
                '''SELECT Qoption.optionID , Qoption.optionTXT, Qoption.nextQ
                   FROM (Qoption
                   INNER JOIN Question ON Qoption.questionID = Question.questionID)
                   WHERE Question.questionID = %s
                   ORDER BY Qoption.optionID ASC''',[questionID])
            res2 = sqlcursor.fetchall()
            sqlcursor.close()
            #save option data in a list
            opt_data = []                       #init list
            for entry in res2:                  #temp will contain current option data 
                temp = {'optID' : entry[0],
                        'opttxt' : entry[1],
                        'nextqID' : entry[2]}
                opt_data.append(temp)           #append temp on option list
            ret_data['options'] = opt_data      #add key options with the option data list as its value 
            if form == 'csv':
                return generateCSVresponse(ret_data, listKey=None, filename=("%s.csv",[questionID])), 200
            else:
                return jsonify(ret_data), 200  #TODO: Check that the json file is returned 
        else:
            return jsonify({
                        "type":"/errors/authentication-error",
                        "title": "Unauthorized User",
                        "status": "401",
                        "detail":"User is unauthorized",
                        "instance":"/question/{}/{}".format(questionnaireID, questionID)}), 401 
    except Exception as error:
        return jsonify({
                    "type":"/errors/unknown",
                    "title": "Error",
                    "status": "500",
                    "detail": error,
                    "instance":"/question/{}/{}".format(questionnaireID, questionID)}), 500