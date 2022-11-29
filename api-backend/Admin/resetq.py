from flask import Flask,render_template, request, Blueprint, jsonify, Response
#from flask_mysqldb import MySQL
import mysql.connector
from mysqlconfig import *

resetq_blueprint = Blueprint("resetq", __name__)

@resetq_blueprint.route('/resetq/<questionnaireID>', methods = ['POST', 'GET'])
def resetq(questionnaireID):
    if request.method == 'GET':
        return jsonify({"status":"failed", "reason":"GET is invalid in resetq"}), 400
        
    if request.method == 'POST':
        sqlcursor = myconnector.cursor()
        sqlcursor.execute(''' SELECT * FROM Answer WHERE (qnrID = %s)''',
        (str(questionnaireID),))
        result = sqlcursor.fetchall()
        if len(result) == 0:
            return jsonify({"status":"failed", "reason":"No answers found"}), 400
        sqlcursor.execute(''' DELETE FROM Answer WHERE (qnrID = %s)''',(str(questionnaireID),))
        sqlcursor.execute(''' COMMIT''')
        sqlcursor.close()
        return jsonify({"status":"OK"})
