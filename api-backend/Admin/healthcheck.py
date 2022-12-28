from flask import Blueprint,  jsonify, request
import mysql.connector
from mysqlconfig import *
from authentication import authAdmin
from csvResponse import generateCSVresponse

healthcheck= Blueprint("healthcheck", __name__)

@healthcheck.route("/healthcheck", methods=["GET"])
# Administrative endpoint for ensuring end-to-end 
# connectivity from backend to database.
def healthcheckf():
    form = request.args.get("format", None)
    if form not in ['json', 'csv']:
        form = 'json'             
    # Verify Admin
    if authAdmin():
        if myconnector.is_connected():
            #myconnector.close() not sure
            #we use database name : "intelliq" as connection string
            output = {"status":"OK", "dbconnection":"intelliq"}
        else:
            output = {"status":"failed", "dbconnection":"intelliq"}
        if form == 'json':
            return jsonify(output), 200
        if form == 'csv':
            return generateCSVresponse(output, listKey=None, filename="healthcheck.csv"), 200
    else:
        return jsonify({
                    "type":"/errors/authentication-error",
                    "title": "Unauthorized User",
                    "status": "401",
                    "detail":"User is unauthorized",
                    "instance":"/admin/healthcheck"}), 401      