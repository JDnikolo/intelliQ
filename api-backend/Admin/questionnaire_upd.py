from service import myconnector
from flask import request, Response, jsonify, Blueprint
from authentication import authAdmin
import json
#TODO: Add remaining bad data checks. 

questionnaire_upd = Blueprint("questionnaire_upd", __name__) 

@questionnaire_upd.route("/questionnaire_upd", methods=["POST"])
def admin_questionnaire_upd():
    if request.method == 'POST':
        try:
            if authAdmin():
                sqlcursor = myconnector.cursor(buffered=True)
                #Check if a file was uploaded
                if 'a' not in request.files:            # use postman post request with form-data, 'a' is the key associated with test json file
                    return Response("No file uploaded.",status = 400)
                temp = request.files['a']
                q = json.load(temp)                     #parse JSON file
                if q:                                   #get json data
                    qnID = q['questionnaireID']          
                    qTitle = q['questionnaireTitle']
                    keywords = q['keywords']
                    questions = q['questions']
                    #Check if questionnaireID already exists
                    sqlcursor.execute("SELECT questionnaireID FROM questionnaire WHERE questionnaireID=%s", [qnID])
                    q_res = sqlcursor.fetchall()                                                
                    if len(q_res) != 0 :             #if it does, return corresponding error
                        return Response("Questionnaire ID already exists.", status=400)
                    sqlcursor.execute(               #else insert data to db, start with questionnaire table  
                    "INSERT INTO questionnaire (questionnaireID,title) VALUES (%s,%s)", [qnID, qTitle])
                    for keyword in keywords:
                        sqlcursor.execute(          #insert keywords on keywords table  
                        "INSERT INTO keywords (questionnaireID,word) VALUES (%s,%s)", [qnID, keyword])
                    #insert questionnaire questions into the database 
                    for question in questions:    
                        #TODO Check if there are any badly written strings in current question dictionary
                        qID = question['qID']
                        qtext = str(question['qtext'])
                        if(question['required'] == 'TRUE'):
                            required = int(1)
                        else:
                            required = int(0)
                        qtype = question['type']
                        sqlcursor.execute(      #insert current question on questions table  
                            "INSERT INTO question (questionID,qtext,required,qtype,qnrID) VALUES (%s,%s,%s,%s,%s)", [qID, qtext, required, qtype, qnID])
                    for question in questions:
                        qID = question['qID']
                        #insert options of current question into the database
                        for option in question['options']:
                                optID = option['optID']
                                text = option['opttxt']
                                nextq = option['nextqID']
                                if nextq == "-" :           #if nextq is "-" (null) adjust query appropriately
                                    sqlcursor.execute(      #inserts current option on option table  
                                        "INSERT INTO qoption (optionID,optionTXT,questionID) VALUES (%s,%s,%s)", [optID, text, qID])
                                else:                       
                                    sqlcursor.execute(      #inserts current option on option table  
                                        "INSERT INTO qoption (optionID,optionTXT,nextQ,questionID) VALUES (%s,%s,%s,%s)", [optID, text, nextq, qID])
                    #all done, commit changes and return success message
                    myconnector.commit()
                    sqlcursor.close()
                    return Response("Questionnaire inserted successfully.",status = 200)
                else:
                    return Response("Bad file.", status = 400)
            else:        
                return jsonify({"type": "/errors/authorization-error",
                    "title": "Unauthorized.",
                    "status": "401",
                    "detail": "You are not authorized to use this endpoint.",
                    "instance": "/admin/questionnaire_upd"}), 401
        except Exception as error:
            return Response("Error.", status = 500)