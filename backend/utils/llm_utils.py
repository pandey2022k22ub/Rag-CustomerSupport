import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configure the Gemini API ---
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    
    genai.configure(api_key=gemini_api_key)
    
    # --- THIS IS THE FIX ---
    # The model name has been updated to 'gemini-2.0-flash' to match
    # your working Node.js implementation, which is the correct model.
    model = genai.GenerativeModel('gemini-2.0-flash')
    logging.info("Gemini 2.0 Flash model initialized successfully.")

except Exception as e:
    logging.error(f"Failed to configure Gemini API: {e}")
    model = None

def generate_response(user_query: str, context: str, sentiment_label: str) -> str:
    """
    Generates a response using the Gemini LLM, incorporating context and sentiment.
    """
    if not model:
        logging.error("Gemini model is not available. Cannot generate response.")
        return "I'm sorry, but my AI service is currently unavailable."

    # Crafting a prompt that uses the retrieved context and sentiment
    prompt = f"""
    You are a helpful and empathetic customer support agent.
    Your customer has expressed a sentiment of: "{sentiment_label}".
    
    Based on the following information from our knowledge base, please answer the user's query.
    If the context doesn't contain the answer, say that you don't have enough information.
    Do not make up information.

    ---
    Knowledge Base Context:
    {context}
    ---

    User's Query: "{user_query}"

    Your Empathetic Response:
    """

    try:
        logging.info("Sending prompt to Gemini API...")
        response = model.generate_content(prompt)
        logging.info("Successfully received response from Gemini API.")
        return response.text
    except Exception as e:
        logging.error(f"An error occurred while calling the Gemini API: {e}", exc_info=True)
        return "I'm sorry, I encountered an error while trying to process your request."
