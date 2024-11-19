import pymsql
import mysql.connector

ENDPOINT = 'tempify-database.cls2ygsysfhs.eu-north-1.rds.amazonaws.com'
PORT = 3306
USER = 'admin'
PASSWORD = 'asdfghjklt-ghniuhgvcwetyiops-dcvnhjhfd2'
DATABASE_NAME = 'Tempify'

try:
    connection = pymsql.connect(
        host = ENDPOINT,
        port = PORT,
        user = USER,
        password = PASSWORD,
        database = DATABASE_NAME
     )
except Exception as e:
    print("Database Connection Failed Due To: {}.".format(e))
