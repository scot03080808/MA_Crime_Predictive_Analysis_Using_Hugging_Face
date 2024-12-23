import tweepy
import pandas as pd
import time
import os

# Twitter API credentials
bearer_token = "AAAAAAAAAAAAAAAAAAAAAIQexgEAAAAAL2zolD%2FI40zJM7%2BA%2BUUmu%2Fc3mwM%3DIyPFqLNlly53o4j4pQU2hWvqhWGAypUz8mWx5cDFoxIIayYC04"

# Authenticate using Bearer Token for API v2
client = tweepy.Client(bearer_token=bearer_token)

# Cities in Massachusetts
cities = ["Boston", "Worcester", "Springfield", "Cambridge", "Lowell", "South Hadley", "Waltham", "New Bedford",
          "Fall River", "Plymouth", "Amherst", "Newton"]

# Define crime categories as lists
violent_crimes = ["assault", "homicide", "murder", "robbery", "rape"]
non_violent_crimes = ["theft", "fraud", "vandalism", "burglary", "shoplifting"]
count = 0

# Rate limit handler
def handle_rate_limit(response_headers):
    """Check response headers and pause if the rate limit is reached."""
    print(f"Headers: {response.headers}")
    remaining = int(response.headers.get("x-rate-limit-remaining", 0))
    reset_time = int(response.headers.get("x-rate-limit-reset", 0))
    if remaining < 4:  # Ensure at least 4 fetches are available
        wait_time = reset_time - int(time.time())
        print(f"Not enough fetches left. Pausing for {wait_time / 60:.2f} minutes...")
        time.sleep(wait_time + 1)  # Add 1-second buffer


# Collect tweets
data = []
for city in cities:
    count += 1
    print(f'the city count is {city} count = {count}')
    query = f"({' OR '.join(violent_crimes + non_violent_crimes)}) {city} -is:retweet lang:en"
    next_token = None  # Initialize the next_token for pagination
    fetch_max_accumulator = 0  # Limit to 4 fetches per city (400 tweets max)
    print(f'the query is {query}')
    while fetch_max_accumulator < 4:
        try:
            print(f'the city is {city} the accumulator is {fetch_max_accumulator}')
            # Fetch tweets
            response = client.search_recent_tweets(
                query=query,
                max_results=100,
                next_token=next_token,
                tweet_fields=["text", "created_at"]
            )
            # Handle rate limit after each fetch
            handle_rate_limit(response.headers)
            remaining_in_fetch = int(response.headers.get("x-rate-limit-remaining", 0))
            # Process tweets
            tweets = response.data
            print(f"This is fetch number {fetch_max_accumulator} for {city} Remaining fetches = {remaining_in_fetch}.")
            if tweets:
                for tweet in tweets:
                    print(tweet.text)
                    data.append({
                        "City": city,
                        "Crime Type": tweet.text,  # Store tweet text for later analysis with TextBlob
                    })
            else:
                print(f"No more tweets found for {city}. Moving to the next city.")
                break  # Exit pagination for this city if no tweets are found

            # Get the next_token for pagination
            next_token = response.meta.get("next_token")
            if not next_token:
                break  # Exit the loop if there are no more pages of tweets

            # Increment the fetch counter
            fetch_max_accumulator += 1

            # Print the fetch count
            print(f"Completed fetch #{fetch_max_accumulator} for {city}.")

        except tweepy.TooManyRequests:
            print("Rate limit hit. Pausing for 15 minutes...")
            time.sleep(15 * 60)  # Wait 15 minutes

        except tweepy.TweepyException as e:
            print(f"Error fetching tweets for {city}: {e}")
            break  # Exit loop on other errors

    # Save progress to CSV after each city
    df = pd.DataFrame(data)
    df.to_csv("classified_crime_tweets.csv", mode='a', index=False, header=not os.path.exists("classified_crime_tweets.csv"))

print("Tweet collection completed. Data saved to 'classified_crime_tweets.csv'.")