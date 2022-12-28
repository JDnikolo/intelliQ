from flask import Blueprint, request, jsonify, Response
from mysqlconfig import *
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))

doAnswer = Blueprint("doAnswer", __name__) 
# static_folder="static", template_folder="template"

@doAnswer.route('/<questionnaireID>/<questionID>/<session>/<optionID>',methods=["GET","POST"])
def answerQS(questionnaireID, questionID, session, optionID):
    if request.method == "GET":
        return Response("<h1>Bad Request</h1><body>GET Request not allowed</body>", status= 400)
    if request.method == "POST":
        print("Did we get here?")
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

        if (sqlcursor.fetchone() == None):
            return jsonify({
                    "type":"/errors/database-operation-failure",
                    "title": "Database Operation Failure",
                    "status": "400",
                    "detail":"Bad request parameters".format(myconnector.database),
                    "instance":"/user/{}/{}/{}/{}".format(questionnaireID, questionID, session, optionID)}), 400
        
        insertAns = '''INSERT INTO `intelliq`.`Answer` (`answerID`, `sessionID`, `ans_optionID`, `qnrID`)
        VALUES ('{}', '{}', '{}', '{}')'''.format(get_random_string(11),session,optionID,questionnaireID)
        sqlcursor.execute(insertAns)
        myconnector.commit()

        sqlcursor.close()
    return Response(status=200)