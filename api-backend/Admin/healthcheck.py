from flask import Blueprint,  jsonify, request
from mysqlconfig import myconnector
from authentication import authAdmin
from csvResponse import generateCSVresponse

healthcheck= Blueprint("healthcheck", __name__)

@healthcheck.route("/healthcheck", methods=['POST', 'GET'])
# Administrative endpoint for ensuring end-to-end 
# connectivity from backend to database.
def healthcheckf():
    if request.method == "POST":
        return jsonify({
                        "type":"/errors/method-not-allowed",
                        "title": "Method Not Allowed",
                        "status": "400",
                        "detail":"POST Request not allowed.",
                        "instance":"/admin/healthcheck"}), 400    #405
    if request.method == "GET":
        args = request.args
        if (len(args) == 0):
                format = "json"
        elif (len(args) > 1):
            return jsonify({"type": "/errors/operation-error",
                        "title": "Invalid query parameters.",
                        "status": "400",
                        "detail": "Only format is acceptable query parameter.",
                        "instance": "/admin/healthcheck"}), 400
        elif (len(args) == 1):
            temp = args.to_dict()
            temp = temp.keys()
            temp = list(temp)
            temp = temp[0]
            if (temp != "format"):
                return jsonify({"type": "/errors/operation-error",
                        "title": "Invalid query parameters.",
                        "status": "400",
                        "detail": "Only format is acceptable query parameter.",
                        "instance": "/admin/healthcheck"}), 400
            elif (args.get("format") == "json"):
                format = "json"
            elif (args.get("format") == "csv"):
                format = "csv"
            else:
                return jsonify({"type": "/errors/operation-error",
                        "title": "Invalid format type.",
                        "status": "400",
                        "detail": "Only json and csv are acceptable formats.",
                        "instance": "/admin/healthcheck"}), 400
            
        # Verify Admin
        if authAdmin():
            if myconnector.is_connected():
                #myconnector.close() not sure
                #we use database name : "intelliq" as connection string
                output = {"status":"OK", "dbconnection":"intelliq"}
            else:
                output = {"status":"failed", "dbconnection":"intelliq"}
            if format == 'json':
                return jsonify(output), 200
            if format == 'csv':
                return generateCSVresponse(output, listKey=None, filename="healthcheck.csv"), 200
        else:
            return jsonify({
                        "type":"/errors/authentication-error",
                        "title": "Unauthorized User",
                        "status": "401",
                        "detail":"User is unauthorized",
                        "instance":"/admin/healthcheck"}), 401      