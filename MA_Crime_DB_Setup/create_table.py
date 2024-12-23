import mysql.connector
import csv


def create_table(csv_file, db_name, table_name, host, user, password):
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password)
        cursor = connection.cursor()

        # Connect to the new database
        connection.database = db_name

        # Read the CSV file to extract column names and data
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Get the first row as column names
            data = list(reader)  # Get the rest of the rows as data

        # Generate the CREATE TABLE statement
        columns = ", ".join([f"`{col}` VARCHAR(255)" for col in headers])
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns})"
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created in database '{db_name}'.")

        # Insert the CSV data into the table
        placeholders = ", ".join(["%s"] * len(headers))
        insert_query = f"INSERT INTO `{table_name}` ({', '.join(headers)}) VALUES ({placeholders})"
        cursor.executemany(insert_query, data)
        print(f"{len(data)} rows inserted into '{table_name}'.")

        # Commit the changes
        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        pass