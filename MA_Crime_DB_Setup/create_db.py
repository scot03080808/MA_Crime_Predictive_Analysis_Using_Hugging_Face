import mysql.connector
from mysql.connector import Error

def create_database(host, user, password, db_name):
    try:
        connection = mysql.connector.connect(
            host=host,  # Replace with your host if different
            user=user,
            password=password
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f'CREATE DATABASE {db_name};')
            print("Database created successfully.")
            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error: {e}")
