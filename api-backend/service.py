from flask import Flask

app = Flask(__name__)

##TODO connect to database

@app.route("/",methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"
##method parameters can be <variables> 
@app.route("/<name>",methods=["GET"])
##variables must be included as keyword arguements
def hello_named(name=""):
    return "<p>Hello, {}!</p>".format(name)