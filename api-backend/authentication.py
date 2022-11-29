from flask import request
from mysqlconfig import myconnector


# Returns True if an endpoint's request contains a valid access token in the X-OBSERVATORY-AUTH header.
# Returns False otherwise.
def authUser():
    uid = request.headers.get("X-OBSERVATORY-AUTH")
    # TODO move user authenticaton here
    if uid == None:
        # None -> custom header not included in request
        return False
    cursor = myconnector.cursor()
    cursor.execute(
        "SELECT * from Users WHERE access_token=%s",
        [uid])
    results = cursor.fetchall()
    cursor.close()
    if len(results) == 0:
        # token does not match any other in the server
        return False
    else:
        # token exists in DB, consider user authenticated
        return True


def authAdmin():
    # TODO implement admin authentication here
    # possibly using authentication strings of mysql.User table
    uid = request.headers.get("X-OBSERVATORY-AUTH")
    if uid == None:
        # None -> custom header not included in request
        return False
    cursor = myconnector.cursor()
    cursor.execute(
        "SELECT * from mysql.User WHERE authentication_string=%s",
        [uid])
    results = cursor.fetchall()
    cursor.close()
    if len(results) == 0:
        # token does not match any other in the server
        return False
    else:
        # token exists in DB, consider user authenticated
        return True
