from mysqlconfig import myconnector
from flask import Blueprint, request, Response
from authentication import authUser
# uuid module is used to create unique identifiers based
# uuid4 creates completely random identifiers without any parameters
from uuid import uuid4

login = Blueprint("login", __name__)
logout = Blueprint("logout", __name__)


@login.route("/login", methods=["POST"])
# logs in a user by creating a unique access token
def loginf():
    if request.headers.get("Content-Type") != "application/x-www-form-urlencoded":
        # invalid content type for logging in
        return Response("Credentials must be x-www-form-urlencoded.", 400)
    sqlcursor = myconnector.cursor()
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
        sqlcursor.close()
        return {"token": uid}, 200
    else:
        sqlcursor.close()
        return Response("Already logged in.", 400)


@logout.route("/logout", methods=["POST"])
def logoutf():
    if not (authUser()):
        return Response("Invalid or missing access token.", 400)
    else:
        uid = request.headers.get("X-OBSERVATORY-AUTH")
        sqlcursor = myconnector.cursor()
        # log user out by revoking their access token
        sqlcursor.execute(
            "UPDATE Users SET access_token=NULL WHERE access_token=%s",
            [uid])
        myconnector.commit()
        return Response("", 200)
