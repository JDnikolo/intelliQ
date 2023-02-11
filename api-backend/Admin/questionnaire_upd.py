from mysqlconfig import *
from flask import request, jsonify, Blueprint
from authentication import authAdmin
import json


questionnaire_upd = Blueprint("questionnaire_upd", __name__) 

@questionnaire_upd.route("/questionnaire_upd", methods=["POST"])
def admin_questionnaire_upd():
    if request.method == 'POST':
        try:
            if authAdmin():
                sqlcursor = myconnector.cursor(buffered=True)
                #Check if a file was uploaded
                if 'file' not in request.files:            # use postman post request with form-data, 'file' is the key associated with test json file
                    return jsonify({
                            "type":"/errors/invalid-input",
                            "title": "Bad Request",
                            "status": "400",
                            "detail":"No file uploaded.",
                            "instance":"/admin/questionnaire_upd"}), 400
                temp = request.files['file']
                try:
                    q = json.load(temp)                     #parse JSON file
                    if q:                                   #get json data
                        try:
                            qnID = q['questionnaireID']          
                            qTitle = q['questionnaireTitle']
                            keywords = q['keywords']
                            questions = q['questions']
                            #Check if questionnaireID already exists
                            sqlcursor.execute("SELECT questionnaireID FROM Questionnaire WHERE questionnaireID=%s", [qnID])
                            q_res = sqlcursor.fetchall()                                                
                            if len(q_res) != 0 :             #if it does, return corresponding error
                                sqlcursor.close()
                                return jsonify({
                                        "type":"/errors/conflict",
                                        "title": "Conflict",
                                        "status": "400",
                                        "detail":"Questionnaire ID already exists.",
                                        "instance":"/admin/questionnaire_upd"}), 400
                            uid = request.headers.get("X-OBSERVATORY-AUTH")
                            sqlcursor.execute(
                                "SELECT username from Users WHERE access_token=%s AND us_role='A'",
                                [uid])
                            username = sqlcursor.fetchall()
                            for user in username:
                                username = user[0]
                            sqlcursor.execute(               #else insert data to db, start with questionnaire table  
                            "INSERT INTO Questionnaire (questionnaireID,title, created_by) VALUES (%s,%s,%s)", [qnID, qTitle,username])
                            for keyword in keywords:
                                sqlcursor.execute(          #insert keywords on keywords table  
                                "INSERT INTO Keywords (questionnaireID,word) VALUES (%s,%s)", [qnID, keyword])
                            #insert questionnaire questions into the database 
                            for question in questions:    
                                qID = question['qID']
                                qtext = str(question['qtext'])
                                if(question['required'] == 'TRUE'):
                                    required = int(1)
                                else:
                                    required = int(0)
                                qtype = question['type']
                                sqlcursor.execute(      #insert current question on questions table  
                                    "INSERT INTO Question (questionID,qtext,required,qtype,qnrID) VALUES (%s,%s,%s,%s,%s)", [qID, qtext, required, qtype, qnID])
                            for question in questions:
                                qID = question['qID']
                                #insert options of current question into the database
                                for option in question['options']:
                                        optID = option['optID']
                                        text = option['opttxt']
                                        nextq = option['nextqID']
                                        if nextq == "-" :           #if nextq is "-" (null) adjust query appropriately
                                            sqlcursor.execute(      #inserts current option on option table  
                                                "INSERT INTO Qoption (optionID,optionTXT,questionID) VALUES (%s,%s,%s)", [optID, text, qID])
                                        else:                       
                                            sqlcursor.execute(      #inserts current option on option table  
                                                "INSERT INTO Qoption (optionID,optionTXT,nextQ,questionID) VALUES (%s,%s,%s,%s)", [optID, text, nextq, qID])
                            #all done, commit changes and return success message
                            myconnector.commit()
                            sqlcursor.close()
                            return jsonify({
                                    "type":"/success",
                                    "title": "OK",
                                    "status": "200",
                                    "detail":"Questionnaire inserted successfully.",
                                    "instance":"/admin/questionnaire_upd"}), 200
                        except Exception as error:
                            sqlcursor.close()
                            return jsonify({
                                "type":"/errors/invalid-input",
                                "title": "Bad Request",
                                "status": "400",
                                "detail":"Badly formatted json parameters.",
                                "instance":"/admin/questionnaire_upd"}), 400
                except Exception as error:
                    return jsonify({
                            "type":"/errors/invalid-input",
                            "title": "Bad Request",
                            "status": "400",
                            "detail":"Wrong file format.",
                            "instance":"/admin/questionnaire_upd"}), 400
            else:        
                return jsonify({
                        "type": "/errors/authorization-error",
                        "title": "Unauthorized.",
                        "status": "401",
                        "detail": "You are not authorized to use this endpoint.",
                        "instance": "/admin/questionnaire_upd"}), 401
        except Exception as error:
            return jsonify({
                    "type":"/errors/unknown",
                    "title": "Error",
                    "status": "500",
                    "detail": error,
                    "instance":"/admin/questionnaire_upd"}), 500