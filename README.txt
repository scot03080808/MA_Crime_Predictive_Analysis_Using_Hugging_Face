This project was used to enhance an analysis done on a data set that included
MA crime records during year of 2010. To be more specific, it tracks different kind
of crimes.  All different types of crimes are then grouped into two different bins.
This project uses data from two different years and also includes unemployment rates during those year.

The primary goal is to use a series of libraries to capture and export the data into a mysql
database.  Then use data persistence to allow us to use python libraries to analyze the data.  This analysis
primarily uses Hugging Face Transformers to analyze 500 random imported crime related tweets from the city
of Boston that were made during 2022.  The Transformers library uses Piplines to analyze a text field to determine
the probability of whether the tweet is a violent and non-violent crime.  When running the main code (main.py) data will be
produced in the terminal that shows the probability that the library function is that it correctly analyzed the tweet as one of the two different categories.
Based on these results each tweet is grouped into the correct categorical bin. This will be displayed in the console.



Below is a list of steps to run this system.
1.a.Install mysql connector run: pip install mysql-connector-python
1.b.If running the requirements.txt file didn't install all necessary packages.  You may need to check some classes imports and run additional pip install imports for thos packages.
1.  Download and unzip this package and note the package location
2.  Download mysql and mysql work bench and run a local instance of mysql to make it accessible.
3.  Go to MA_Crime_DB_Setup/db_main.py and modify the database fields to reflect your local environment in order to create a connection to your sql server.
4.  Also, update the file path within db_main.py to reflect where this package is located and where the .csv files to be uploaded are located.
5.  Run "pip install -r requirements.txt" within your pycharm or other IDE terminal to install all the necessary libraries needed to run the code.
6.  Within sqlserver workbench right click on the database pane (you might need to adjust the Navigator pane from 'Administration' to 'Schemas' within the bottom of the Navigator pane)
 and select "refresh all" (if you don't see the newly created database), then Verify that the database and two tables where created and are populated with data.
7.  Go to main.py and update database credentials to reflect your local environment.
8.  Analyze results in the terminal.
9.  Feel free to add to the project ideas include:

A. Populating more data from different years and use transformers to create a predictive model for future years based on population
and unemployment rates.

B. Compare the city of Boston results to another city of a different size and determine how the size of a city population
effects crime.

C. Use my x_data_collection.py method to grab tweets in real time before using your monthly api call allowance.

Some issues I encountered were the following:

1.  Originally I intended to use 'X' tweepy 2.0 api to import a series of tweets in real time and then user the Hugging Face Transformers tool to interpret the conversational AI.
Unfortunately, the free tier developer account is restricted to a total of no more than 1,500 total tweets.  Also, it restricts users from accessing the api more than 300 times every 15 minuest.

I left the class in the code x_data_collection.py in the package.  You'll see that I created a method to handle the rate limit.
Unfortunately, by the time my code was working well I had already extracted the total number of tweets allowed per month using the free tier

To address this issue I created a class that uses the csv and random library to create random violent and non-violent crime tweets:

tweet_csv_creation.py

This class creates an adjustable amount of fake tweets using a list of violent and non-violent key words.
Also, the amount of violent or non-violent tweets is also adjustable.
It then uses the csv library to create the tweets csv that is used to generate the crime_tweets table in our ma_crime database.

This code is available for download in github@

https://github.com/scot03080808/MA_Crime_Predictive_Analysis_Using_Hugging_Face/tree/master

Feel free to pull down you own local environment and make pull requests if you'd like to extend on to this project.

David Scott