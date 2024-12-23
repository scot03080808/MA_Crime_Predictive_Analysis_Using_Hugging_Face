from transformers import pipeline

# Initialize Hugging Face zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define our two labels
candidate_labels = ["violent_crime", "non_violent_crime"]


def classify_tweets(tweets):
    results = []
    for t in tweets:
        text = t["tweet_text"]
        classification = classifier(text, candidate_labels)
        # classification['labels'] is sorted by confidence desc
        label = classification['labels'][0]
        score = classification['scores'][0]

        results.append({
            "tweet_id": t["tweet_id"],
            "text": text,
            "predicted_label": label,
            "confidence": score
        })
    return results
# Classify tweets from both periods
# classified_period_a = classify_tweets(tweets_period_a)

def compute_percentages(classified_tweets):
    violent_count = sum(1 for c in classified_tweets if c["predicted_label"] == "violent_crime")
    non_violent_count = len(classified_tweets) - violent_count
    total = len(classified_tweets)
    if total == 0:
        return 0, 0
    violent_pct = (violent_count / total) * 100
    non_violent_pct = (non_violent_count / total) * 100
    return violent_pct, non_violent_pct

# violent_pct_a, non_violent_pct_a = compute_percentages(classified_period_a)
# violent_pct_b, non_violent_pct_b = compute_percentages(classified_period_b)