# db_connector.py
# This class uses the sqlalchemy library to establish a connection to the mysql database
# It allows the software to fetch data and execute sql statements using the methods below.

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text

class DatabaseConnector:
    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.engine = self._create_engine()

    def _create_engine(self):
        ### Create a SQLAlchemy engine.
        db_url = f'mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
        return create_engine(db_url)

    def fetch_data(self, query):
        ### Execute a query and return the results as a Pandas DataFrame
        return pd.read_sql(query, self.engine)

    def execute_query(self, query):
        with self.engine.connect() as connection:
            trans = connection.begin()  # Begin transaction
            try:
                connection.execute(text(query))
                trans.commit()  # Explicitly commit
            except Exception as e:
                trans.rollback()  # Rollback on error
                print(f"An error occurred: {e}")
                raise
