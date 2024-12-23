import tweepy
import pandas as pd
import time

# Twitter API credentials
bearer_token = "Your Token"

# Authenticate using Bearer Token for API v2
client = tweepy.Client(bearer_token=bearer_token)

# Cities in Massachusetts
cities = ["Boston", "Worcester", "Springfield", "Cambridge", "Lowell", "South Hadley", "Waltham", "New Bedford", "Fall River", "Plymouth", "Amherst", "Newton"]

crime_categories = {
    "Violent Crimes": ["assault", "homicide", "murder", "robbery", "arson", "rape"],
    "Non-Violent Crimes": ["theft", "fraud", "vandalism", "burglary", "shoplifting", "embezzlement"]
}


# Rate limit handler
def handle_rate_limit(response_headers):
    """Check response headers and pause if the rate limit is reached."""
    remaining = int(response_headers.get("x-rate-limit-remaining", 0))
    reset_time = int(response_headers.get("x-rate-limit-reset", 0))

    if remaining == 0:
        # Calculate wait time until reset
        wait_time = reset_time - int(time.time())
        print(f"Rate limit reached. Pausing for {wait_time / 60:.2f} minutes...")
        time.sleep(wait_time + 1)  # Add 1-second buffer


# Collect tweets
data = []
for city in cities:
    for category, keywords in crime_categories.items():
        for keyword in keywords:
            query = f"{keyword} {city} -is:retweet lang:en"
            print(f'Query for {city}: {query}')
            try:
                # Fetch tweets
                response = client.search_recent_tweets(query=query, max_results=100, tweet_fields=["text", "created_at"],
                                                       return_response=True)

                # Handle rate limit using response headers
                handle_rate_limit(response.headers)

                # Process tweets
                tweets = response.data
                if tweets:
                    for tweet in tweets:
                        data.append({
                            "City": city,
                            "Crime Category": category,
                            "Keyword": keyword,
                            "Tweet": tweet.text,
                            "Created At": tweet.created_at
                        })
                        print(f'the current data is.....................................{data}')
                else:
                    print(f"No tweets found for {keyword} in {city} ({category})")

            except tweepy.TweepyException as e:
                print(f"Error fetching tweets for {keyword} in {city} ({category}): {e}")

# Save data to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("classified_crime_tweets.csv", index=False)

print("Tweet collection completed. Data saved to 'classified_crime_tweets.csv'.")