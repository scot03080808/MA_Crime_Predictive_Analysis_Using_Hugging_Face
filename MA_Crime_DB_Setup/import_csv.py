import pandas as pd
import numpy as np  # Import numpy to handle NaN
import mysql.connector
from mysql.connector import Error

def upload_csv_to_mysql(file_path, host, database, user, password, table_name):
    # Connect to MySQL database
    print(f'the value of arguments when calling upload_csv_to_mysql are file_path = {file_path}, host = {host}, database = {database}, user = {user}, password = {password}, table_name = {table_name}')
    connection = mysql.connector.connect(
        file_path=file_path,
        host=host,
        database=database,
        user=user,
        password=password,
        table_name = table_name
    )
    cursor = connection.cursor()
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
        print(f"CSV file '{file_path}' read successfully.")

        # Replace string 'NULL' with numpy.nan (Pandas interprets this as a missing value)
        df.replace('NULL', np.nan, inplace=True)

        if connection.is_connected():
            print("Connected to MySQL database")
            # Dynamically create a table based on the DataFrame's column names and inferred data types
            column_definitions = []
            for col in df.columns:
                if df[col].dtype == 'int64':
                    col_type = 'INT'
                elif df[col].dtype == 'float64':
                    col_type = 'FLOAT'
                elif df[col].dtype == 'bool':
                    col_type = 'BOOLEAN'
                elif pd.api.types.is_datetime64_any_dtype(df[col]):
                    col_type = 'DATETIME'
                else:
                    col_type = 'VARCHAR(255)'  # Default to VARCHAR for string-like data
                column_definitions.append(f"`{col}` {col_type}")

            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS `{table_name}` (
                {', '.join(column_definitions)}
            );
            """
            cursor.execute(create_table_query)
            print(f"Table '{table_name}' created or verified to exist.")

            # Insert data row by row
            for _, row in df.iterrows():
                # Convert the row to a tuple, with None for NaN values (interpreted as NULL by MySQL)
                values = tuple(None if pd.isna(value) else value for value in row)
                placeholders = ", ".join(["%s"] * len(row))
                insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({placeholders})"
                cursor.execute(insert_query, values)

            # Commit changes
            connection.commit()
            print(f"Data from '{file_path}' successfully uploaded to '{table_name}'.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

