from create_db import create_database
from create_table import create_table
from db_connector import DatabaseConnector

# Database connection details
DB_USERNAME = 'root'
DB_PASSWORD = 'Camar098'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'ma_crime'
CRIME_CSV_FILE_PATH = 'C:/Users/scot0/603Homework/Project/603_Project_DScott/MA_Crime_DB_Setup/MA-crime-employment.csv'
TWEET_CSV_FILE_PATH = 'C:/Users/scot0/603Homework/Project/603_Project_DScott/MA_Crime_DB_Setup/crime_tweets_500.csv'

# #Step 1 Create database
create_database(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)

# Step 2: Upload MA-crime-employment.csv into mysql database.
create_table(CRIME_CSV_FILE_PATH,DB_NAME, 'ma_crime_unemployment', DB_HOST, DB_USERNAME, DB_PASSWORD)
# Step 3: Alter and update MA-crime-employment database with new fields for oct 2024 and populate values
db_connector = DatabaseConnector(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

alter_table = """
ALTER TABLE ma_crime.ma_crime_unemployment
ADD COLUMN Non_Violent_Crimes_per_10_000_2010 INT,
ADD COLUMN Violent_Crimes_per_10_000_2010 INT,
ADD COLUMN Total_Crimes_per_10_000_2010 INT,
ADD COLUMN Population_2022 INT,
ADD COLUMN Unemployment_Rate_2022 DOUBLE,
ADD COLUMN Non_Violent_Crimes_per_10_000_2022 INT,
ADD COLUMN Violent_Crimes_per_10_000_2022 INT,
ADD COLUMN Total_Crimes_per_10_000_2022 INT;
"""

db_connector.execute_query(alter_table)
print("Table altered successfully.")

# Step 3: Add values new values for 2022 to the city of Boston
update_table = """
UPDATE ma_crime.ma_crime_unemployment
SET
Non_Violent_Crimes_per_10_000_2010 = 437,
Violent_Crimes_per_10_000_2010 = 110,
Total_Crimes_per_10_000_2010 = 547,
Violent_Crimes_per_10_000_2022 = 45,
Non_Violent_Crimes_per_10_000_2022 = 217,
Total_Crimes_per_10_000_2022 = 262,
Unemployment_Rate_2022 = 3.5,
Population_2022 = 654423
WHERE city = 'Boston';
"""

db_connector.execute_query(update_table)
print('Updated table ma_crime table successfully.')
#
# #Step 3: Create boston_tweets table and populate it with the values included in boston_tweets_2.0.csv
create_table(TWEET_CSV_FILE_PATH,'ma_crime', 'crime_tweets', DB_HOST, DB_USERNAME, DB_PASSWORD)
print("crime_tweets table created")