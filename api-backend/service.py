from mysqlconfig import *
from flask import Flask, jsonify, request, render_template
from mysqlconfig import myconnector
from flask import Flask
from Users.doAnswer import doAnswer
from Users.question import question
from Admin.questionnaire_upd import questionnaire_upd
from Users.loginout import *
from Users.questionnaireid import *
from Users.getsessionanswers import *
from Users.getquestionanswers import *
from Admin.resetall import *
from Admin.usermod import *
from Admin.resetall import resetall
from Admin.healthcheck import healthcheck
from Admin.resetq import *
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(resetall, url_prefix="/intelliq_api/admin")
app.register_blueprint(usermod, url_prefix="/intelliq_api/admin")
app.register_blueprint(healthcheck, url_prefix="/intelliq_api/admin")
app.register_blueprint(users, url_prefix="/intelliq_api/admin")
app.register_blueprint(resetq_blueprint, url_prefix="/intelliq_api/admin")
app.register_blueprint(login, url_prefix="/intelliq_api")
app.register_blueprint(logout, url_prefix="/intelliq_api")
app.register_blueprint(questionnaireid, url_prefix="/intelliq_api")
app.register_blueprint(getsessionanswers_blueprint, url_prefix="/intelliq_api")
app.register_blueprint(getquestionanswers_blueprint,
                       url_prefix="/intelliq_api")
app.register_blueprint(doAnswer, url_prefix="/intelliq_api")
app.register_blueprint(questionnaire_upd, url_prefix="/intelliq_api/admin")
app.register_blueprint(question, url_prefix="/intelliq_api")

# /etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf
# change base url TODO: uncomment this
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

CORS(app)

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
