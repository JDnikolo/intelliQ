from Users.loginout import *
from Users.questionnaireid import *
from Users.getsessionanswers import *
from Admin.resetall import *
from Admin.usermod import *
from Admin.resetall import resetall
from Admin.healthcheck import healthcheck
from Admin.resetq import *
#uncomment 2 following lines to add questionnaire_upd and question endpoints
from Admin.questionnaire_upd import questionnaire_upd
from Users.question import question
from flask import Flask, jsonify, request, render_template
from mysqlconfig import *

app = Flask(__name__)

app.register_blueprint(resetall, url_prefix="/admin")
app.register_blueprint(usermod, url_prefix="/admin")
app.register_blueprint(healthcheck, url_prefix="/admin")
app.register_blueprint(users, url_prefix="/admin")
app.register_blueprint(resetq_blueprint, url_prefix="/admin")
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(questionnaireid)
app.register_blueprint(getsessionanswers_blueprint, url_prefix="")
#uncomment 2 following lines to add questionnaire_upd and question endpoints
app.register_blueprint(questionnaire_upd, url_prefix="/admin")
app.register_blueprint(question)

# /etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf
# change base url TODO: uncomment this
# app.config["APPLICATION_ROOT"] = "/intelliq_api"
app.config["JSON_SORT_KEYS"] = False
# # mysqlconfig.py template
# import mysql.connector
# myconnector = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="#poupass",
#    database='intelliq',
#    port=3306
# )
# sqlcursor.execute(sql_query) to access database
sqlcursor = myconnector.cursor(buffered=True)
# buffered was set to true to fetch more than 1 rows https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone
# TODO remove testing endpoints when actual endpoints are
# ready to use
# method parameters can be <variables>


@app.route("/", methods=["GET"])
def hello_world():
    sqlcursor.execute("SHOW TABLES")
    result = sqlcursor.fetchall()
    return f"<p>{(result)}</p>"


# method parameters can be <variables>
@app.route("/test/<name>", methods=["GET"])
# variables must be included as keyword arguements
def hello_named(name=""):
    return "<p>Hello, {}!</p>".format(name)


if __name__ == "__main__":
    app.run(port=9000, debug=True)
