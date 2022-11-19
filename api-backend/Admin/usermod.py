from service import app, sqlcursor, myconnector
from flask import request, jsonify, Response
# TODO: ensure that calling user is an admin


@app.route("/admin/usermod/<username>/<password>", methods=["POST"])
# Administrative endpoint for creating users and
# modifying passwords of existing users.
def usermod(username: str, password: str):
    if (username == "" or password == ""):
        return Response("Empty Required Fields", status=400)
    if (len(username) > 10 or len(password) > 20):  # could be implemented using try-catch
        return Response("Bad Request Parameters", status=400)
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
    return Response("", 200)


@app.route("/admin/users/<username>", methods=["GET"])
# Admin endpoint for retrieving user information.
def users(username: str):
    keys = ["username", "password", "access_token"]
    if (username == ""):
        return Response("", status=400)
    sqlcursor.execute("SELECT * FROM Users WHERE username=%s", [username])
    results = sqlcursor.fetchall()
    if len(results) == 0:
        # 402 apparently corresponds to "Payment needed???"
        return Response("", status=402)
    else:
        output = {keys[i]: results[0][i] for i in range(0, 3, 2)}
        return jsonify(output)
