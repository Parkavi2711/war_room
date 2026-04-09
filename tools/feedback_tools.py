import json
from collections import Counter

NEGATIVE_KEYWORDS = [
    "crash", "slow", "slower", "freeze",
    "broke", "bug", "issue", "problem",
    "unacceptable", "lag"
]

POSITIVE_KEYWORDS = [
    "love", "nice", "good", "great",
    "clean", "cool", "helped"
]


def load_feedback(json_path: str) -> list:
    """
    Load feedback entries from JSON file.
    """
    with open(json_path, "r") as f:
        return json.load(f)


def analyze_feedback(feedback_entries: list) -> dict:
    """
    Perform simple sentiment classification and issue extraction.
    """
    sentiment = {
        "positive": 0,
        "neutral": 0,
        "negative": 0
    }

    issue_counter = Counter()

    for entry in feedback_entries:
        text = entry["feedback"].lower()

        if any(word in text for word in NEGATIVE_KEYWORDS):
            sentiment["negative"] += 1
            for word in NEGATIVE_KEYWORDS:
                if word in text:
                    issue_counter[word] += 1

        elif any(word in text for word in POSITIVE_KEYWORDS):
            sentiment["positive"] += 1

        else:
            sentiment["neutral"] += 1

    return {
        "sentiment_distribution": sentiment,
        "top_issues": issue_counter.most_common(5),
        "total_feedback": len(feedback_entries)
    }
