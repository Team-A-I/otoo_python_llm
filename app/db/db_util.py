# db_util.py
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='model_db',
            user='otoo',
            password='1234'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)

def get_model_name():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT model_name FROM model_config ORDER BY id DESC LIMIT 1")
    model_name = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return model_name
