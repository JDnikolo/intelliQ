import mysql.connector
# Replace the MySQL host, port and user details below as necessary
# then rename this file to mysqlconfig.py.
myconnector = mysql.connector.connect(
    host="yourhost",
    user="hostuser",
    password="userpassword",
    database='intelliq',  # DO NOT CHANGE THIS
    port=3306
)
