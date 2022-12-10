from flask import Blueprint,  jsonify
import mysql.connector
from mysqlconfig import *
from authentication import authAdmin

healthcheck= Blueprint("healthcheck", __name__)

@healthcheck.route("/healthcheck", methods=["GET"])
# Administrative endpoint for ensuring end-to-end 
# connectivity from backend to database.
def healthcheckf():
    
    # Verify Admin
    if authAdmin():
        if myconnector.is_connected():
            #myconnector.close() not sure
            #we use database name : "intelliq" as connection string
            return jsonify({"status":"OK", "dbconnection":"intelliq"}), 200
        else:
            return jsonify({"status":"failed", "dbconnection":"intelliq"}), 200
    else:
        return jsonify({
                    "type":"/errors/authentication-error",
                    "title": "Unauthorized User",
                    "status": "401",
                    "detail":"User is unauthorized",
                    "instance":"/admin/healthcheck"}), 401 
     
#enallaktika: 
#def healthcheckf():
    try:
        connection = mysql.connector.connect(   host="localhost",
                                                user="root",
                                                password="",
                                                database='intelliq',
                                                port=3306
                                            )
        if connection.is_connected():
            return ({"status":"OK", "dbconnection":"intelliq"}), 200
        #we use database name : "intelliq" as connection string
        else:
            return jsonify({"status":"failed", "dbconnection":"intelliq"}), 200
        
    finally:
        if connection.is_connected():
            connection.close()        