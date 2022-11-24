from flask import Flask, jsonify, request, render_template
import mysql.connector
from mysqlconfig import *

app = Flask(__name__)
from Admin.resetall import resetall
app.register_blueprint(resetall, url_prefix="/admin")
# /etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf 
# change base url TODO: uncomment this
# app.config["APPLICATION_ROOT"] = "/intelliq_api"
# TODO: change port to 91003 as specified in project_softeng2022_part2_v01
app.config["JSON_SORT_KEYS"] = False
# # mysqlconfig.py template
""" mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",
   database='intelliq',
   port=3306
) """
# sqlcursor.execute(sql_query) to access database
sqlcursor = myconnector.cursor(buffered=True)
# buffered was set to true to fetch more than 1 rows https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone
# TODO remove testing endpoints when actual endpoints are
# ready to use
from Admin.usermod import *
from Admin.resetall import *
from Users.loginout import *

# method parameters can be <variables>
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

if __name__ == "__main__":
    app.run(port=91003, debug=True)