import os
import sys
import pytest

# Add backend root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.rag_services import rag_query


def test_rag_query_basic():
    """Test if RAG query returns all required keys."""
    query = "How can I reset my account password?"
    result = rag_query(query)

    # Check required keys
    assert "retrieved_articles" in result
    assert "sentiment" in result
    assert "ai_response" in result

    # Check types
    assert isinstance(result["retrieved_articles"], list)
    assert isinstance(result["sentiment"], dict)
    assert isinstance(result["ai_response"], str)


def test_rag_query_with_sentiment_integration():
    """Test if sentiment label is one of expected values."""
    query = "I am really unhappy with your service."
    result = rag_query(query)

    assert result["sentiment"]["label"] in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
