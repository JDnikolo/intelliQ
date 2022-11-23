from flask import Flask, jsonify, request
import mysql.connector
from mysqlconfig import *


app = Flask(__name__)

# change base url TODO: uncomment this
# app.config["APPLICATION_ROOT"] = "/intelliq_api"
# TODO: change port to 91003 as specified in project_softeng2022_part2_v01
app.config["JSON_SORT_KEYS"] = False
# # mysqlconfig.py template
# import mysql.connector
# myconnector = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="",
#    database='intelliq',
#    port=3306
# )
# sqlcursor.execute(sql_query) to access database
sqlcursor = myconnector.cursor()
# TODO remove testing endpoints when actual endpoints are
# ready to use
from Admin.usermod import *
from Users.loginout import *
#uncomment the following  line to add question test endpoint.
#from Users.question import *

@app.route("/", methods=["GET"])
def hello_world():
    sqlcursor.execute("SHOW TABLES")
    result = sqlcursor.fetchall()
    return f"<p>{(result)}</p>"


# method parameters can be <variables>
@app.route("/<name>", methods=["GET"])
# variables must be included as keyword arguements
def hello_named(name=""):
    return "<p>Hello, {}!</p>".format(name)
