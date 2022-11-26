from service import myconnector
from flask import jsonify, Response, Blueprint

#TODO add authorization

question = Blueprint("question", __name__) 

@question.route("/question/<questionnaireID>/<questionID>", methods=["GET"])
def usr_question(questionnaireID: str, questionID: str):
    try:
        sqlcursor = myconnector.cursor(buffered=True)
        #if qnrID doesnt have QQxyz format, or qID doesnt have Pxy format, return bad request code
        #if ((len(questionnaireID) != 5) or (len(questionID) != 3)):
        #    return Response("Required fields were not given or they are incorrectly formatted", status=400)
        #else check if they exist in the database.
        #SQL Query for checking
        sqlcursor.execute(
            '''SELECT questionnaire.questionnaireID ,question.questionID, question.qtext,question.required,question.qtype
               FROM (questionnaire
               INNER JOIN question ON questionnaire.questionnaireID = question.qnrID)
               WHERE (questionnaire.questionnaireID = %s AND question.questionID = %s)''',[questionnaireID, questionID])
        res = sqlcursor.fetchall()
        if len(res) == 0:
            return Response("The requested questionnaire/question is not present in the database ", status=400) 
        #save query data to return object
        for info in res:
            ret_data = {'questionnaireID' : info[0],
                        'qID' : info[1],
                        'qtext' : info[2],
                        'required' : str(info[3]),   #potentially need to convert 0/1 to false/true string here
                        'type' : info[4]}            
        #fetch options sorted by optID keys.
        sqlcursor.execute(
            '''SELECT qoption.optionID , qoption.optionTXT, qoption.nextQ
               FROM (qoption
               INNER JOIN question ON qoption.questionID = question.questionID)
               WHERE question.questionID = %s
               ORDER BY qoption.optionID ASC''',[questionID])
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
        return jsonify(ret_data), 200  #TODO: Check that the json file is returned 
    except Exception as error:
        return Response(error, status = 500)