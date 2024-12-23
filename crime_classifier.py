# crime_classifier.py
from transformers import pipeline

class CrimeClassifier:
    def __init__(self):
        # Define crime categories as lists
        self.violent_crimes = ["assault", "homicide", "murder", "robbery", "rape"]
        self.non_violent_crimes = ["theft", "fraud", "vandalism", "burglary", "shoplifting"]

    def classify_crime(self, tweet):
        """Classify a single tweet based on crime-related keywords."""
        tweet_lower = tweet.lower()  # Convert tweet to lowercase for case-insensitive matching

        # Check for violent crime keywords
        if any(keyword in tweet_lower for keyword in self.violent_crimes):
            return "violent"

        # Check for non-violent crime keywords
        elif any(keyword in tweet_lower for keyword in self.non_violent_crimes):
            return "non-violent"

        # If no keywords are found
        else:
            return "unknown"


    def classify_dataset(self, data, text_column):
        """Apply classification to a DataFrame."""
        data['crime_type'] = data[text_column].apply(self.classify_crime)
        data['crime_type'].value_counts()
        return data
