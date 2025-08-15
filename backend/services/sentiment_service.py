# services/sentiment_service.py
from transformers import pipeline

# Load sentiment analysis model once
sentiment_pipeline = pipeline("sentiment-analysis")

def detect_sentiment(text: str):
    """Detect sentiment (Positive/Negative/Neutral) from text."""
    result = sentiment_pipeline(text)[0]
    return {
        "label": result["label"],
        "score": round(result["score"], 2)
    }
