from service import app, sqlcursor, myconnector
from flask import request, Response
# uuid module is used to create unique identifiers based
# uuid4 creates completely random identifiers without any parameters
from uuid import uuid4


@app.route("/login", methods=["POST"])
# logs in a user by creating a unique access token
def login():
    if request.headers.get("Content-Type") != "application/x-www-form-urlencoded":
        # invalid content type for logging in
        return Response("Credentials must be x-www-form-urlencoded.", 400)
    username = request.form["username"]
    password = request.form["password"]
    sqlcursor.execute(
        "SELECT access_token from Users WHERE username=%s AND us_password=%s",
        [username, password])
    result = sqlcursor.fetchall()
    if len(result) == 0:
        # either password or username was incorrect,
        return Response("Invalid Credentials", 400)
    if result[0][0] == None or result[0][0] == "":
        uid = uuid4().hex[:30]
        # user isn't already logged in, create access token and return it
        sqlcursor.execute(
            "UPDATE Users SET access_token=%s WHERE username=%s AND us_password=%s",
            [uid, username, password])
        myconnector.commit()
        return {"token": uid}, 200
    else:
        return Response("Already logged in.", 400)


@app.route("/logout", methods=["POST"])
def logout():
    uid = request.headers.get("X-OBSERVATORY-AUTH")
    if uid == None:
        # None -> custom header not included in request
        return Response("No access token provided.", 400)
    sqlcursor.execute(
        "SELECT * from Users WHERE access_token=%s",
        [uid])
    results = sqlcursor.fetchall()
    if len(results) == 0:
        # access key doesn't exist, return
        return Response("Invalid access token", 400)
    else:
        # log user out by revoking their access token
        sqlcursor.execute(
            "UPDATE Users SET access_token=NULL WHERE access_token=%s",
            [uid])
        myconnector.commit()
        return Response("", 200)
