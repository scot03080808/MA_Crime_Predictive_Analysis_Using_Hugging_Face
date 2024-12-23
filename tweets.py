import pandas as pd
from Demos.win32ts_logoff_disconnected import username
from PyQt5.QtSql import password
from sphinx.search import parse_stop_word
from sqlalchemy import create_engine
from transformers import pipeline

from MA_Crime_DB_Setup.db_main import db_connector
from db_connector import DatabaseConnector

class Tweets(DatabaseConnector):
    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        database_connection = DatabaseConnector(username, password, host, port, database)
        query = '''SELECT * FROM ma_crime_unemployment cu
                   INNER JOIN crime_tweets ct on ct.city = cu.city'''

        self.data = db_connector.fetch_data(query)

    # Load the crime_tweets table into a DataFrame
    def analyze_data(self):

        # Display the first few rows
        header = self.data.head()

        # Get a concise summary of the DataFrame
        info = self.data.info()

        # Generate descriptive statistics
        statistics = self.data.describe(include='all')

        # Check for missing values in each column
        missing_value = self.data.isnull().sum()

        # Calculate the percentage of missing values per column
        missing_percentage = self.data.isnull().mean() * 100

        analysis_dict = {'header' : header, 'info' : info, 'statistics' : statistics, 'missing_value' : missing_value, 'missing_percentage': missing_percentage}

        return analysis_dict

    # Classification function
    def classify_crime(tweet):
        # Load pre-trained text classification pipeline
        classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        result = classifier(tweet)[0]
        if "violent" in result['label'].lower():
            return "violent"
        elif "non-violent" in result['label'].lower():
            return "non-violent"
        else:
            return "unknown"

    # Apply classification
    self.data['crime_type'] = db_connector['text'].apply(classify_crime)

    # Count the classifications
    print(self.data['crime_type'].value_counts())