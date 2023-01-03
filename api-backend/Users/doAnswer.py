from flask import Blueprint, request, jsonify, Response
from mysqlconfig import *
import random
import string
from datetime import datetime

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def ansIdFromTimestamp():
    rawStamp = datetime.now().strftime("%y%m%d%H%M%S")
    centuries = chr(64+int(rawStamp[:2]))
    return centuries + (rawStamp[2:])

doAnswer = Blueprint("doanswer", __name__) 
# static_folder="static", template_folder="template"

@doAnswer.route('/doanswer/<questionnaireID>/<questionID>/<session>/<optionID>',methods=["GET","POST"])
def answerQS(questionnaireID, questionID, session, optionID):
    if request.method == "GET":
        return jsonify({"status": "400 Bad request parameters"}), 400
    if request.method == "POST":
        # check parameters validity
        if(len(session) > 4 or len(questionID)  > 20 or len(questionnaireID) > 5 or len(optionID)  > 20):
            return jsonify({
                    "type":"/errors/database-operation-failure",
                    "title": "Database Operation Failure",
                    "status": "400",
                    "detail":"Bad request parameters",
                    "instance":"/user/{}/{}/{}/{}".format(questionnaireID, questionID, session, optionID)}), 400
        try:
            sqlcursor = myconnector.cursor(buffered=True)
        except:
            return jsonify({
                    "type":"/errors/database-operation-failure",
                    "title": "Database Operation Failure",
                    "status": "500",
                    "detail":"Could not get handle to {}".format(myconnector.database),
                    "instance":"/{}/{}/{}/{}".format(questionnaireID, questionID, session, optionID)}), 500
        # verify that post is conducted on existing data
        sqlcursor.execute('''SELECT `questionID` FROM `Question` WHERE `Question`.`qnrID` = '{}';'''.format(questionnaireID))
        questionDB = sqlcursor.fetchall()
        if ( questionDB == None or not any(x[0] == questionID for x in questionDB)):
            return jsonify({
                    "type":"/errors/database-operation-failure",
                    "title": "Database Operation Failure",
                    "status": "400",
                    "detail":"Bad request parameters",
                    "instance":"/user/{}/{}/{}/{}".format(questionnaireID, questionID, session, optionID)}), 400
        

        # verify that optionID exists for this Question and get details
        stmt = "SELECT `optionID` FROM `Qoption` WHERE `Qoption`.`questionID` = '%s' AND `Qoption`.`optionID` = '%s'" % (str(questionID),str( optionID))
        sqlcursor.execute(stmt)
        optionQuery = sqlcursor.fetchone()
        if (optionQuery == None):
            return jsonify({
                        "type":"/errors/database-operation-failure",
                        "title": "Database Operation Failure",
                        "status": "400",
                        "detail":"Bad request parameters, option does not exist for this question",
                        "instance":"/user/{}/{}/{}/{}".format(questionnaireID, questionID, session, optionID)}), 400
        # Check if it is an open-ended question
        if (optionQuery[0] == "<open string>"):
            #TODO: Get answer text from front-end form
            pass
        else:
            if (optionID != optionQuery[0]):
                return jsonify({
                        "type":"/errors/database-operation-failure",
                        "title": "Database Operation Failure",
                        "status": "400",
                        "detail":"Bad request parameters",
                        "instance":"/user/{}/{}/{}/{}".format(questionnaireID, questionID, session, optionID)}), 400
            else:
                sqlcursor.execute('''SELECT `optionTXT` FROM `Qoption` WHERE `Qoption`.`questionID` = %s AND `Qoption`.`optionID` = %s;''', [questionID, optionID])
                answerTXT = sqlcursor.fetchone()[0]

        insertAns = '''INSERT INTO `intelliq`.`Answer` (`answerID`, `sessionID`, `ans_optionID`, `qnrID`, `answertxt`)
VALUES ('{}', '{}', '{}', '{}', '{}')'''.format(ansIdFromTimestamp(), session, optionID, questionnaireID, answerTXT)
        sqlcursor.execute(insertAns)
        myconnector.commit()

        sqlcursor.close()
    return jsonify({"status": "Successful"}), 200