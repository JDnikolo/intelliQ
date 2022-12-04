from flask import Blueprint, request, jsonify, Response
from authentication import authAdmin
from mysqlconfig import *

resetall = Blueprint("nuke", __name__) 
# static_folder="static", template_folder="template"
resetall.before_app_first_request(authAdmin)
@resetall.route("/nuke", methods=["GET","POST"])
def adminResetall():
    if authAdmin():
        if request.method == "GET":
            return Response("<h1>Bad Request</h1><body>GET Request not allowed</body>"), 400
        if request.method == "POST":
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

            # Get all tables
            query = '''SELECT TABLE_NAME 
                FROM information_schema.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='intelliq' '''
            try:
                sqlcursor.execute(query)
                # Put table names in a list variable
                allTables = sqlcursor.fetchall()
            except:
                return jsonify({
                        "type":"/errors/database-operation-failure",
                        "title": "Database Operation Failure",
                        "status": "500",
                        "detail":"Could not fetch Database Tables",
                        "instance":"/admin/resetall"}), 500
            for table in allTables:
                # Delete all entries for each table
                try:
                    sqlcursor.execute(f'''DELETE FROM `intelliq`.{table[0]};''')
                    myconnector.commit()
                except:
                    return jsonify({
                        "type":"/errors/database-operation-failure",
                        "title": "Database Operation Failure",
                        "status": "500",
                        "detail":"Table '{}'.'{}' could not be deleted".format(myconnector.database,table),
                        "instance":"/admin/resetall"}), 500
                
            sqlcursor.close()
            
            return Response("Database Deleted"), 200
    else:
        return "<h1>Think you are the Admin, boy?</h1>"