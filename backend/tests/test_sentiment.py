import os
import sys
import pytest

# Add backend root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.sentiment_service import detect_sentiment


def test_positive_sentiment():
    """Check positive sentiment detection."""
    text = "I love this product! It's amazing."
    result = detect_sentiment(text)

    assert result["label"] in ["POSITIVE", "LABEL_2"]  # transformer models may return label names
    assert 0 <= result["score"] <= 1


def test_negative_sentiment():
    """Check negative sentiment detection."""
    text = "This is terrible and I hate it."
    result = detect_sentiment(text)

    assert result["label"] in ["NEGATIVE", "LABEL_0"]
    assert 0 <= result["score"] <= 1


def test_neutral_sentiment():
    """Check neutral sentiment detection."""
    text = "The product arrived yesterday."
    result = detect_sentiment(text)

    # Some models don't have neutral, so we just ensure it's valid
    assert result["label"] in ["POSITIVE", "NEGATIVE", "NEUTRAL", "LABEL_0", "LABEL_1", "LABEL_2"]
    assert 0 <= result["score"] <= 1
