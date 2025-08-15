import logging
from services.article_service import search_articles
# This is the corrected import. It now calls the 'analyze' function.
from services.sentiment_service import analyze as analyze_sentiment
from utils.llm_utils import generate_response

async def generate_answer(query: str, sources: list, sentiment: dict, tone: str = None):
    """
    This function runs the full RAG pipeline.
    """
    logging.info("--- [RAG Service] Starting RAG pipeline ---")
    
    # The context is prepared from the sources passed in from the chat route
    context = "\n\n".join([f"Title: {s.get('title', '')}\nContent: {s.get('snippet', '')}" for s in sources])
    
    try:
        # Call the llm_utils function that connects to the Gemini API
        response_text = generate_response(
            user_query=query, 
            context=context, 
            sentiment_label=sentiment.get("label", "neutral")
        )
        return response_text
    except Exception as e:
        logging.error(f"--- [RAG Service] ERROR during LLM call: {e}", exc_info=True)
        return "I'm sorry, but I encountered an error trying to generate a response."
