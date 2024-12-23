import csv
import random

# Violent crime keywords
violent_crimes = [
    "murder", "assault", "battery", "robbery", "kidnapping", "arson",
    "sexual assault", "manslaughter", "aggravated assault", "stalking",
    "domestic violence", "hate crime", "vehicular homicide"
]

# Non-violent crime keywords
non_violent_crimes = [
    "theft", "vandalism", "trespassing", "fraud", "forgery", "embezzlement",
    "identity theft", "tax evasion", "possession of stolen property",
    "reckless driving", "disorderly conduct", "public intoxication",
    "illegal gambling"
]

# We want 6.6% violent crime tweets out of 500 total = 33 violent, 467 non-violent
NUM_VIOLENT = 33
NUM_NON_VIOLENT = 455

# Simple templates for tweets
violent_template = [
    "Multiple reports of {crime} just came in.",
    "Authorities are investigating an incident involving {crime}.",
    "Police received a tip about ongoing {crime} in the area."
]

non_violent_template = [
    "A case of {crime} was reported earlier today.",
    "Officials are looking into {crime} at a local establishment.",
    "Local police responded to a {crime} call from a resident."
]

def generate_violent_tweets(num):
    tweets = []
    for _ in range(num):
        crime = random.choice(violent_crimes)
        template = random.choice(violent_template)
        tweet_text = template.format(crime=crime)
        tweets.append(tweet_text)
    return tweets

def generate_non_violent_tweets(num):
    tweets = []
    for _ in range(num):
        crime = random.choice(non_violent_crimes)
        template = random.choice(non_violent_template)
        tweet_text = template.format(crime=crime)
        tweets.append(tweet_text)
    return tweets

violent_tweets = generate_violent_tweets(NUM_VIOLENT)
non_violent_tweets = generate_non_violent_tweets(NUM_NON_VIOLENT)

# Combine and shuffle
all_tweets = violent_tweets + non_violent_tweets
random.shuffle(all_tweets)

# Write to CSV with headers: city, tweet
with open("crime_tweets_500.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["city", "tweet"])
    # We'll just hard-code city as "Boston" (or any city you want)
    for tw in all_tweets:
        writer.writerow(["Boston", tw])

print("CSV file 'crime_tweets_500.csv' created with 500 tweets.")