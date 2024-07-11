# db_util.py
import mysql.connector
from mysql.connector import Error
import os

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def get_model_name():
    connection = get_db_connection()
    if connection is None:
        raise Exception("Failed to connect to database")
    cursor = connection.cursor()
    cursor.execute("SELECT model_name FROM model_config ORDER BY model_code DESC LIMIT 1")
    result = cursor.fetchone()
    model_name = result[0] if result else None
    cursor.close()
    connection.close()
    return model_name
