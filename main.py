# main.py
from db_connector import DatabaseConnector
from tweet_analysis_transformers import classify_tweets, compute_percentages
from sqlalchemy import create_engine
import pandas as pd

# Database connection details
DB_USERNAME = 'root'
DB_PASSWORD = 'Camar098'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'ma_crime'

db_connector = DatabaseConnector(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

# Step 1: Fetch data from the database and analyze the data
query = '''
 SELECT cu.Non_Violent_Crimes_per_10_000_2010, cu.Violent_Crimes_per_10_000_2010, cu.Total_Crimes_per_10_000_2010,
 cu.Unemployment_Aug_2010, cu.Non_Violent_Crimes_per_10_000_2022, cu.Violent_Crimes_per_10_000_2022, cu.Total_Crimes_per_10_000_2022, 
 ct.id, ct.crime_tweets
 FROM ma_crime_unemployment cu
 INNER JOIN crime_tweets ct ON ct.city = cu.city
 '''
print(f'the query is {query} fetching now')

data = db_connector.fetch_data(query) # Display the first few rows
columns = [
    "Non_Violent_Crimes_per_10_000_2010", "Violent_Crimes_per_10_000_2010", "Total_Crimes_per_10_000_2010",
    "Unemployment_Aug_2010", "Non_Violent_Crimes_per_10_000_2022", "Violent_Crimes_per_10_000_2022",
    "Total_Crimes_per_10_000_2022"
]

df = pd.DataFrame(data, columns=columns)
print("Data fetched successfully:")
print(df)

# Initialize dictionary for access to the query values outside of the for loop
crime_data_dict = []

# Store all the data in a dictionary
for index, row in df.iterrows():
    crime_data_dict.append({column: row[column] for column in df.columns})


# Rename the tweet columns to match what classify_tweets transformer method expects
data = data.rename(columns={
    'id': 'tweet_id',
    'crime_tweets': 'tweet_text'
})

# extract only needed columns
data_as_dicts = data[['tweet_id', 'tweet_text']].to_dict('records')
results = classify_tweets(data_as_dicts)
print(f'the results of the tweet_analysis using pipeline from  transformers is {results}')

violent_pct_a, non_violent_pct_a = compute_percentages(results)
print(f'Violent crime tweets:   {violent_pct_a:.2f}%')
print(f'Non-violent crime tweets: {non_violent_pct_a:.2f}%')
print()
# "Non_Violent_Crimes_per_10_000_2010", "Violent_Crimes_per_10_000_2010", "Total_Crimes_per_10_000_2010",
# "Unemployment_Aug_2010", "Non_Violent_Crimes_per_10_000_2022", "Violent_Crimes_per_10_000_2022",
# "Total_Crimes_per_10_000_2022"
# Step 2 compare the results of the tweet analysis compared to the reported violent and non-violent crime rate
# based on mass.gov that persists in the mysql db.
# recorded_violent_crimes_2022 = data[['non-violent', 'Non_Violent_Crimes_per_10_000_2022']]

# header = data.head() # Get a concise summary of the DataFrame
# info = data.info() # Generate descriptive statistics
# statistics = data.describe(include='all') # Check for missing values in each column
# missing_value = data.isnull().sum() # Calculate the percentage of missing values per column
# missing_percentage = data.isnull().mean() * 100
# analysis_dict = {'header': header, 'info': info, 'statistics': statistics, 'missing_value': missing_value,
#                  'missing_percentage': missing_percentage}
#
# for key in analysis_dict:
#     print(f'For {key} the result is {analysis_dict[key]}')

# Step 2: Classify tweets
# tweet_analysis = classify_tweets(data)




# classifier = CrimeClassifier()
# classified_data = classifier.classify_dataset(data, text_column='crime_tweets') # Classify as either violent or non-violent crime
#
# # Step 3: Display results
# print(classified_data['crime_type'].value_counts())






