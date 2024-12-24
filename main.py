# main.py
from MA_Crime_DB_Setup.tweet_csv_creation import non_violent_crimes
from db_connector import DatabaseConnector
from tweet_analysis_transformers import classify_tweets, compute_percentages
import pandas as pd

# step 1: install mysql and determine the values of the following credentials.
# NOTE: Credentials will be different for each user and where you store the package from this system.

# Database connection details
DB_USERNAME = 'root'
DB_PASSWORD = 'Camar098'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'ma_crime'

db_connector = DatabaseConnector(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
### Step 2: run db_main.py file within the MA_Crime_DB_Setup folder prior to running this.  The db_main.py
### uses .csv files located within this package to setup the data needed to run the main.py file.
### NOTE: only run the db_main.py file one time.

### Step 2: Fetch data from the database and analyze the data
query = '''
 SELECT id, crime_tweets
 FROM crime_tweets 
 WHERE city = 'Boston'
 '''
print(f'Fetching tweets from crime_tweets table in the database.', end="\n\n")

data = db_connector.fetch_data(query)

### Step 3: analyze the data using the results from the database.  Use Transformers to determine
### the probability that the crime commited within the tweet is violent or non-violent.  Then assign each
### tweet to the appropriate categorical bin.

# Rename the tweet columns to match what classify_tweets transformer method expects
data = data.rename(columns={
    'id': 'tweet_id',
    'crime_tweets': 'tweet_text'
})

# extract only needed columns
data_as_dicts = data[['tweet_id', 'tweet_text']].to_dict('records')
results = classify_tweets(data_as_dicts)

# display each tweet as a list of dictionaries that contains the probability of whether the tweet falls into one of the
# two categories based on the Hugging Face transformers analysis.  Note all the tweets are on one line.  This was required depending
# your pycharm settings in order to view all tweets within the list.
print(f'The results of the tweet_analysis using pipeline from  transformers is {results}', end = "\n\n")

# Displays total percentage of violent and non-violent crimes using transformers.
violent_pct_a, non_violent_pct_a = compute_percentages(results)
print(f'Violent crime tweets using hugging face transformers:   {violent_pct_a:.2f}%')
print(f'Non-violent crime tweets using hugging face transformers: {non_violent_pct_a:.2f}%', end= "\n\n")

# Step 4 - Call MA crime data for the city of Boston from the database and assign the data to it's
# Field within a dictionary.
query = """
SELECT population, population_2022, Non_Violent_Crimes_per_10_000_2010, Violent_Crimes_per_10_000_2010, Total_Crimes_per_10_000_2010,
Unemployment_Aug_2010, Non_Violent_Crimes_per_10_000_2022, Violent_Crimes_per_10_000_2022, Total_Crimes_per_10_000_2022, Unemployment_Rate_2022 
FROM ma_crime_unemployment
Where city = 'Boston'
"""

print(f'Fetching the data from the ma_crime_unemployment table in the database')
data = db_connector.fetch_data(query)

columns = [
    "Non_Violent_Crimes_per_10_000_2010", "Violent_Crimes_per_10_000_2010", "Total_Crimes_per_10_000_2010",
    "Unemployment_Aug_2010", "Non_Violent_Crimes_per_10_000_2022", "Violent_Crimes_per_10_000_2022",
    "Total_Crimes_per_10_000_2022", "Unemployment_Rate_2022"
]

df = pd.DataFrame(data, columns=columns)
print("Data fetched successfully:")
# print(df)

# Initialize dictionary for access to the query values outside of the for loop
crime_data_dict = {}

Non_Violent_Crimes_per_10_000_2010 = 0
Violent_Crimes_per_10_000_2010 = 0
Total_Crimes_per_10_000_2010 = 0
Unemployment_Aug_2010 = 0.0
Non_Violent_Crimes_per_10_000_2022 = 0
Violent_Crimes_per_10_000_2022 = 0
Total_Crimes_per_10_000_2022 = 0
Unemployment_Rate_2022 = 0.0
population = 0
population_2022 = 0

# iterate through this data and print it in the console to compare the data.
# Notice that unemployment rate between these two times is significantly different.
# Also, notice that the total number of crime directly correlates with unemployment rates.
for index, row in df.iterrows():
    crime_data_dict[index] = {column: row[column] for column in df.columns}
    # print(f"Row {index} details:")

    for column in df.columns:
        if column == "Non_Violent_Crimes_per_10_000_2010":
            Non_Violent_Crimes_per_10_000_2010 = row[column]
        elif column == "Violent_Crimes_per_10_000_2010":
            Violent_Crimes_per_10_000_2010 = row[column]
        elif column == "Total_Crimes_per_10_000_2010":
            Total_Crimes_per_10_000_2010 = row[column]
        elif column == "Unemployment_Aug_2010":
            Unemployment_Aug_2010 = row[column]
        elif column == "Non_Violent_Crimes_per_10_000_2022":
            Non_Violent_Crimes_per_10_000_2022 = row[column]
        elif column == "Violent_Crimes_per_10_000_2022":
            Violent_Crimes_per_10_000_2022 = row[column]
        elif column == "Total_Crimes_per_10_000_2022":
            Total_Crimes_per_10_000_2022 = row[column]
        elif column == "Unemployment_Rate_2022":
            Unemployment_Rate_2022 = row[column]
        elif column == "population":
            population = row[column]
        elif column == "Population_2022":
            population_2022 = row[column]

        # print(f" {column}: {row[column]}")

violent_crime_pct_2010 = round(Non_Violent_Crimes_per_10_000_2010/Total_Crimes_per_10_000_2010 * 10, 1)
non_violent_crimes_pct_2010 = round(Violent_Crimes_per_10_000_2010/Total_Crimes_per_10_000_2010 * 10, 1)

violent_crime_pct_2022 = round(Violent_Crimes_per_10_000_2022/Total_Crimes_per_10_000_2022 * 10, 1)
non_violent_crimes_pct_2022 = round(Non_Violent_Crimes_per_10_000_2022/Total_Crimes_per_10_000_2022 * 10, 1)

# Print 2010 Boston crime and unemployment data
print(f'''
Crime information for city of Boston in 2010: 
Population: {population}
Unemployment rate: {round(Unemployment_Aug_2010,1)}
Non-violent crimes per 10,000: {Non_Violent_Crimes_per_10_000_2010}
Violent crimes per 10,000: {Violent_Crimes_per_10_000_2010}
Total Crimes per 10,000: {int(Total_Crimes_per_10_000_2010)}  
Percentage of violent crime based on total crime in 2010: {violent_crime_pct_2010}
Percentage of non-violent crime based on total crime in 2010: {non_violent_crimes_pct_2010}
''')

# Print 2022 Boston crime and unemployment data
print(f'''
Crime information for city of Boston in 2022: 
Population: {population_2022}
Unemployment rate: {round(Unemployment_Rate_2022,1)}
Total non-violent crimes per 10,000: {Non_Violent_Crimes_per_10_000_2022}
Total violent crimes per 10,000: {Violent_Crimes_per_10_000_2022}
Total crimes per 10,000: {int(Total_Crimes_per_10_000_2022)}.  
Percentage of violent crime based on total crime in 2022: {int(violent_crime_pct_2022)}
Percentage of non-violent crime based on total crime in 2022: {int(non_violent_crimes_pct_2022)}
''')

# Print the difference between the data from both years
print('Difference between crime and unemployment data in Boston based on 2010 vs 2022:')
print(f'''
'Difference between crime and unemployment data in Boston based on 2010 vs 2022:
unemployment rate in 2022 vs 2010: {round(Unemployment_Aug_2010 - Unemployment_Rate_2022, 1)} less.
Total crimes per 10,000 in 2022 vs 2010: {int(Total_Crimes_per_10_000_2010 - Total_Crimes_per_10_000_2022)} less.  
Percentage of violent crime in 2022 vs 2010: {int(violent_crime_pct_2010 - Violent_Crimes_per_10_000_2022)} less.
Non-violent crime in 2022 vs 2010: {int(Non_Violent_Crimes_per_10_000_2010 - Non_Violent_Crimes_per_10_000_2022)} less.
''', end='\n\n')


print('''Tweet values using the hugging face library.  
Notice the difference between the 2022 percentages used by calculating the data using the information available
on mass.gov website.  Then go back to the line in the terminal and take a look at the list of tweet dictionaries.  A
You'll notice that according to Transformers many of the tweets were very close to going one way or another
based on the analysis.''')

print(f'''
Violent crime tweets using hugging face transformers:   {violent_pct_a:.2f}%
Non-violent crime tweets using hugging face transformers: {non_violent_pct_a:.2f}%
vs.
Percentage of violent crime based on total crime in 2022: {int(violent_crime_pct_2022)}
Percentage of non-violent crime based on total crime in 2022: {int(non_violent_crimes_pct_2022)}
''')







