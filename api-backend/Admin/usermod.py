from flask import Blueprint, request, jsonify
from authentication import authAdmin
from mysqlconfig import myconnector
from csvResponse import generateCSVresponse

usermod = Blueprint("usermod", __name__)
users = Blueprint("users", __name__)


@usermod.route("/usermod/<username>/<password>", methods=["POST"])
# Administrative endpoint for creating users and
# modifying passwords of existing users.
def usermodf(username: str, password: str):
    if not authAdmin():
        return jsonify({"type": "/errors/authorization-error",
                        "title": "Unauthorized.",
                        "status": "401",
                        "detail": "You are not authorized to use this endpoint.",
                        "instance": "/admin/usermod"}), 401
    if (username == "" or password == ""):
        return jsonify({"type": "/errors/operation-error",
                        "title": "Missing required fields.",
                        "status": "400",
                        "detail": "Username and/or password are required but are not included in the request.",
                        "instance": "/admin/usermod"}), 400
    if (len(username) > 10 or len(password) > 20):  # could be implemented using try-catch?
        return jsonify({"type": "/errors/operation-error",
                        "title": "Incorrect credential length.",
                        "status": "400",
                        "detail": "Username and/or password are too long.",
                        "instance": "/admin/usermod"}), 400
    sqlcursor = myconnector.cursor()
    sqlcursor.execute("SELECT * FROM Users WHERE username=%s", [username])
    results = sqlcursor.fetchall()
    if len(results) == 0:
        # empty list, no result -> create user
        sqlcursor.execute(
            "INSERT INTO Users (username,us_password,us_role) VALUES (%s,%s,%s)", [username, password, 'V'])
    else:
        if results[0][2] == 'A':
            # user exists but is an admin, abort
            return jsonify({"type": "/errors/operation-error",
                            "title": "No modifying Admin credentials.",
                            "status": "400",
                            "detail": "User {} has the Admin role and their credentials cannot be modified using this endpoint.".format(username),
                            "instance": "/admin/usermod"}), 400
        # user exists, change password
        sqlcursor.execute(
            f"UPDATE Users SET us_password=\"{password}\" WHERE username=\"{username}\"")
    myconnector.commit()
    sqlcursor.close()
    return jsonify({}), 200


@users.route("/users/<username>", methods=["GET"])
# Admin endpoint for retrieving user information.
def usersf(username: str):
    form = request.args.get("format", None)
    if form not in ['json', 'csv']:
        form = 'json'
    if not authAdmin():
        return jsonify({"type": "/errors/authorization-error",
                        "title": "Unauthorized.",
                        "status": "401",
                        "detail": "You are not authorized to use this endpoint.",
                        "instance": "/admin/users"}), 401
    if (username == ""):
        return jsonify({"type": "/errors/operation-error",
                        "title": "Missing required fields.",
                        "status": "400",
                        "detail": "Username is required but is not included in the request.",
                        "instance": "/admin/users"}), 400
    sqlcursor = myconnector.cursor()
    keys = ["username", "password", "user_type", "access_token"]
    sqlcursor.execute("SELECT * FROM Users WHERE username=%s", [username])
    results = sqlcursor.fetchall()
    sqlcursor.close()
    if len(results) == 0:
        # 402 apparently corresponds to "Payment needed???"
        return jsonify({"type": "/errors/operation-error",
                        "title": "No user found.",
                        "status": "402",
                        "detail": "User {} was not found.".format(username),
                        "instance": "/admin/users"}), 402
    else:
        # user exists but is an Admin, abort
        print(results)
        if results[0][2] == 'A':
            return jsonify({"type": "/errors/operation-error",
                            "title": "No retrieving Admin credentials.",
                            "status": "400",
                            "detail": "User {} has the Admin role and their credentials cannot be retrieved using this endpoint.".format(username),
                            "instance": "/admin/users"}), 400
        output = {keys[i]: results[0][i] for i in range(0, 4)}
        if form == 'json':
            return jsonify(output), 200
        if form == 'csv':
            return generateCSVresponse(output, listKey=None, filename="users.csv"), 200
