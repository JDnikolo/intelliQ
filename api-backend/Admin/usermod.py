from flask import Blueprint, request, jsonify, Response
from authentication import authAdmin
from mysqlconfig import myconnector
# TODO: ensure that calling user is an admin

usermod = Blueprint("usermod", __name__)
users = Blueprint("users", __name__)


@usermod.route("/usermod/<username>/<password>", methods=["POST"])
# Administrative endpoint for creating users and
# modifying passwords of existing users.
def usermodf(username: str, password: str):
    if not authAdmin():
        return Response("Unauthorized.", status=401)
    if (username == "" or password == ""):
        return Response("Empty Required Fields", status=400)
    if (len(username) > 10 or len(password) > 20):  # could be implemented using try-catch
        return Response("Bad Request Parameters", status=400)
    sqlcursor = myconnector.cursor()
    sqlcursor.execute("SELECT * FROM Users WHERE username=%s", [username])
    results = sqlcursor.fetchall()
    if len(results) == 0:
        # empty list, no result -> create user
        sqlcursor.execute(
            "INSERT INTO Users (username,us_password) VALUES (%s,%s)", [username, password])
    else:
        # user exists, change password
        sqlcursor.execute(
            f"UPDATE Users SET us_password=\"{password}\" WHERE username=\"{username}\"")
    myconnector.commit()
    sqlcursor.close()
    return Response("", 200)


@users.route("/users/<username>", methods=["GET"])
# Admin endpoint for retrieving user information.
def usersf(username: str):
    if not authAdmin:
        return Response("Unauthorized.", status=401)
    if (username == ""):
        return Response("", status=400)
    sqlcursor = myconnector.cursor()
    keys = ["username", "password", "access_token"]
    sqlcursor.execute("SELECT * FROM Users WHERE username=%s", [username])
    results = sqlcursor.fetchall()
    sqlcursor.close()
    if len(results) == 0:
        # 402 apparently corresponds to "Payment needed???"
        return Response("", status=402)
    else:
        output = {keys[i]: results[0][i] for i in range(0, 3)}
        return jsonify(output)
