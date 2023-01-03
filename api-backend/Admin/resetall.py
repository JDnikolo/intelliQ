from flask import Blueprint, request, jsonify
from authentication import authAdmin
from mysqlconfig import myconnector

resetall = Blueprint("resetall", __name__) 
# static_folder="static", template_folder="template"
resetall.before_app_first_request(authAdmin)
@resetall.route("/resetall", methods=["GET","POST"])
def adminResetall():
    
    if request.method == "GET":
        return jsonify({
                "type":"/errors/method-not-allowed",
                "title": "Method Not Allowed",
                "status": "400",
                "detail":"GET Request not allowed.",
                "instance":"/admin/resetall"}), 400     #405

    if request.method == "POST":
        # Verify Admin
        if authAdmin():
            # Parse error answers as Response.json()[<field>]
            # Get db cursor
            try:
                sqlcursor = myconnector.cursor(buffered=True)
            except:
                return jsonify({
                        "type":"/errors/database-operation-failure",
                        "title": "Database Operation Failure",
                        "status": "500",
                        "detail":"Could not get handle to {}".format(myconnector.database),
                        "instance":"/admin/resetall"}), 500

            uid = request.headers.get("X-OBSERVATORY-AUTH")
            sqlcursor.execute(
            "SELECT * from Users WHERE access_token=%s AND us_role='Admin'",
                [uid])
            username = sqlcursor.fetchone()[0]
            print(username)
            try:
                sqlcursor = myconnector.cursor(buffered=True)
            except:
                return jsonify({
                        "type":"/errors/database-operation-failure",
                        "title": "Database Operation Failure",
                        "status": "500",
                        "detail":"Could not get handle to {}".format(myconnector.database),
                        "instance":"/admin/resetall"}), 500
            # Get questionnaires created by this admin
            query = '''SELECT questionnaireID 
                FROM Questionnaire q INNER JOIN Users u ON q.created_by = u.username 
                WHERE u.username="{}"'''.format(username)
            try:
                sqlcursor.execute(query)
                # Put table names in a list variable
                questionnaires = sqlcursor.fetchall() 
            except:
                return jsonify({
                        "type":"/errors/database-operation-failure",
                        "title": "Database Operation Failure",
                        "status": "500",
                        "detail":"Could not fetch Database Tables",
                        "instance":"/admin/resetall"}), 500
            if (len(questionnaires) == 0):
                return jsonify({
                            "type":"/errors/operation-error",
                            "title": "Questionnaires for the user already Deleted",
                            "status": "400",
                            "detail":"User {} has no available questionnaires".format(username),
                            "instance":"/admin/resetall"}), 400
            for questionnaire in questionnaires:
                # Delete all entries for each table
                try:
                    sqlcursor.execute('''DELETE FROM `intelliq`.`Answer` WHERE `Answer`.`qnrID`= '{}';'''.format(questionnaire[0]))
                    myconnector.commit()
                except:
                    return jsonify({
                            "type":"/errors/database-operation-failure",
                            "title": "Database Operation Failure",
                            "status": "500",
                            "detail":"Entry '{}'.'{}' could not be deleted".format("Answer",questionnaire[0]),
                            "instance":"/admin/resetall"}), 500

                try:
                    sqlcursor.reset()
                    query = '''SELECT qo.optionID FROM `Question` q INNER JOIN `Qoption` qo ON q.questionID = qo.questionID WHERE q.qnrID = '{}';'''.format(questionnaire[0])
                    sqlcursor.execute(query)
                    qoptions = sqlcursor.fetchall()
                except:
                    return jsonify({
                            "type":"/errors/database-operation-failure",
                            "title": "Database Operation Failure",
                            "status": "500",
                            "detail":"{} entries could not be fetched".format(questionnaire[0]),
                            "instance":"/admin/resetall"}), 500
                for qoption in qoptions:
                    try:
                        sqlcursor.execute('''DELETE FROM Qoption WHERE optionID = '{}';'''.format(qoption[0]))
                        myconnector.commit()
                    except:
                        return jsonify({
                        "type":"/errors/database-operation-failure",
                        "title": "Database Operation Failure",
                        "status": "500",
                        "detail":"Entry '{}'.'{}' could not be deleted".format("Qoption",qoption[0]),
                        "instance":"/admin/resetall"}), 500
                try:
                    sqlcursor.execute('''DELETE FROM `intelliq`.`Question` WHERE `Question`.`qnrID`= '{}';'''.format(questionnaire[0]))
                    myconnector.commit()
                except:
                    return jsonify({
                            "type":"/errors/database-operation-failure",
                            "title": "Database Operation Failure",
                            "status": "500",
                            "detail":"Entry '{}'.'{}' could not be deleted".format("Question",questionnaire[0]),
                            "instance":"/admin/resetall"}), 500
                try:
                    sqlcursor.execute('''DELETE FROM `intelliq`.`Keywords` WHERE `Keywords`.`questionnaireID`= '{}';'''.format(questionnaire[0]))
                    myconnector.commit()
                except:
                    return jsonify({
                            "type":"/errors/database-operation-failure",
                            "title": "Database Operation Failure",
                            "status": "500",
                            "detail":"Entry '{}'.'{}' could not be deleted".format("Keywords",questionnaire),
                            "instance":"/admin/resetall"}), 500
                try:
                    sqlcursor.execute('''DELETE FROM `intelliq`.`Questionnaire` WHERE questionnaireID= '{}';'''.format(questionnaire[0]))
                    myconnector.commit()
                except:
                    return jsonify({
                        "type":"/errors/database-operation-failure",
                        "title": "Database Operation Failure",
                        "status": "500",
                        "detail":"Entry '{}'.'{}' could not be deleted".format("Questionnaire",questionnaire[0]),
                        "instance":"/admin/resetall"}), 500
                    # return jsonify({"status":"failed", "reason":"Entry '{}'.'{}' could not be deleted".format("Questionnaire",questionnaire[0])}), 500
                
            sqlcursor.close()
            return jsonify({"status":"OK"}), 200                
            #return Response("Reset Successful"), 200
            return jsonify({"status": "Successful"}), 200
        else:
            return jsonify({
                        "type":"/errors/authentication-error",
                        "title": "Unauthorized User",
                        "status": "401",
                        "detail":"User is unauthorized",
                        "instance":"/admin/resetall"}), 401
