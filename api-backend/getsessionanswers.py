from flask import request, Blueprint, jsonify
import mysql.connector

#TODO: add the following lines in service.py
#from getsessionanswers import getsessionanswers_blueprint
#app.register_blueprint(getsessionanswers_blueprint, url_prefix="")
getsessionanswers_blueprint = Blueprint("getsessionanswers", __name__)

#TODO: somehow remove connection details
#this connection is specific to my configuration, it's not generic
connection = mysql.connector.connect(host='localhost',
                                     database='intelliq',
                                     user='root',
                                     password='')

@getsessionanswers_blueprint.route('/getsessionanswers/<questionnaireID>/<session>', methods = ['POST', 'GET'])
def getsessionanswers(questionnaireID,session):
    if request.method == 'GET':
        sqlcursor = connection.cursor()
        sqlcursor.execute(''' SELECT questionID, answerID FROM Answer INNER JOIN qoption
        WHERE (sessionID = %s AND qnrID = %s)
        ORDER BY questionID''',(str(session),str(questionnaireID)))
        result = sqlcursor.fetchall()
        sqlcursor.close()
        return jsonify({"questionnaireID": str(questionnaireID),
        "session": str(session), "answers": result})
        
    if request.method == 'POST':
        return jsonify({"status":"failed", "reason":"POST is invalid in getsessionanswers"})
        #POST is invalid, return json explaining, as required
