from flask import Flask, jsonify, request
import mysql.connector


app = Flask(__name__)
# TODO move this to another file
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='intelliq',
    port=3306
)
# sqlcursor.execute(sql_query) to access database
sqlcursor = mydb.cursor()


@app.route("/", methods=["GET"])
def hello_world():

    return f"<p>Hello World!</p>"


# method parameters can be <variables>


@app.route("/<name>", methods=["GET"])
# variables must be included as keyword arguements
def hello_named(name=""):
    return "<p>Hello, {}!</p>".format(name)
