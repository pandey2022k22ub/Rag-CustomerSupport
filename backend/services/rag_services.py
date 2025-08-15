# services/rag_services.py
from services.article_service import search_articles
from services.sentiment_service import detect_sentiment
from utils.llm_utils import generate_response

def rag_query(user_query: str):
    """RAG pipeline: retrieve + sentiment + generate empathetic response."""
    # Step 1: Retrieve relevant articles
    articles = search_articles(user_query)

    # Step 2: Analyze sentiment
    sentiment_result = detect_sentiment(user_query)

    # Step 3: Prepare context for LLM
    context = "\n\n".join([f"{a['title']}: {a['content']}" for a in articles])

    # Step 4: Generate empathetic response
    response = generate_response(user_query, context, sentiment_result["label"])

    return {
        "retrieved_articles": articles,
        "sentiment": sentiment_result,
        "ai_response": response
    }
