import mysql.connector  # import mysql connector


# Sets up a connection to a database
def connection():
    connect = mysql.connector.connect(
        host="HOST",
        user="USER",
        passwd="PASS",
        database="DATABASE"
    )
    return connect
