import logging
from transformers import pipeline

# --- Initialize the Sentiment Analysis Pipeline ---
# This uses the Hugging Face transformers library to load a pre-trained model.
# The model will be downloaded automatically the first time this code is run.
try:
    # This specific model is good for general-purpose sentiment analysis.
    sentiment_analyzer = pipeline(
        "sentiment-analysis", 
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )
    logging.info("Sentiment analysis model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load sentiment analysis model: {e}", exc_info=True)
    sentiment_analyzer = None

# This is the 'analyze' function that was missing.
async def analyze(text: str) -> dict:
    """
    Analyzes the sentiment of a given text using the loaded pipeline.
    """
    if not sentiment_analyzer:
        logging.error("Sentiment analyzer is not available.")
        # Return a neutral fallback response if the model failed to load
        return {"label": "NEUTRAL", "score": 0.5}

    try:
        # The pipeline returns a list with a single dictionary, e.g., [{'label': 'POSITIVE', 'score': 0.999}]
        results = sentiment_analyzer(text)
        # We return the first result from the list.
        return results[0]
    except Exception as e:
        logging.error(f"An error occurred during sentiment analysis: {e}", exc_info=True)
        return {"label": "ERROR", "score": 0.0}

