import pymysql
import pandas as pd


def create_db(db_host, db_user, db_password, db_name, csv_filename):
    # CSV file path

    connection = None  # Initialize connection to None
    cursor = None # Initialize cursor to None

    # Connect to the MySQL database
    try:
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()
        print("Connected to the database successfully!")

        # Create a new table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS crime_tweets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city VARCHAR(255),
            crime_tweets TEXT
        );
        """
        cursor.execute(create_table_query)
        print("Table 'crime_tweets' created successfully!")

        # Load the CSV file
        df = pd.read_csv(csv_filename)

        # Insert data into the table
        for index, row in df.iterrows():
            insert_query = """
            INSERT INTO crime_tweets (city, crime_tweets)
            VALUES (%s, %s);
            """
            cursor.execute(insert_query, (row['city'], row['tweet']))

        # Commit changes
        connection.commit()
        print(f"{len(df)} rows inserted into 'crime_tweets' table.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        if connection:
            cursor.close()
            connection.close()
            print("Database connection closed.")
