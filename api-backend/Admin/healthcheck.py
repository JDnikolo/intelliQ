from flask import Blueprint,  jsonify
import mysql.connector
from mysqlconfig import *
# TODO: ensure that calling user is an admin

healthcheck= Blueprint("healthcheck", __name__)

@healthcheck.route("/healthcheck", methods=["GET"])
# Administrative endpoint for ensuring end-to-end 
# connectivity from backend to database.
def healthcheckf():
    if myconnector.is_connected():
        return jsonify({"status":"OK", "dbconnection":"intelliq"}), 200
    else:
        return jsonify({"status":"failed", "dbconnection":"intelliq"}), 200
     
#enallaktika: 
#def healthcheckf():
    try:
        connection = mysql.connector.connect(   host="localhost",
                                                user="root",
                                                password="",
                                                database='intelliq',
                                                port=3306
                                            )
        #TODO: use mysqlconfig.py instead
        if connection.is_connected():
            return ({"status":"OK", "dbconnection":"intelliq"}), 200
        #we use database name : "intelliq" as connection string
        else:
            return jsonify({"status":"failed", "dbconnection":"intelliq"}), 200
        
    finally:
        if connection.is_connected():
            connection.close()        