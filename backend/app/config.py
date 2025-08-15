# app/config.py
import os
from dotenv import load_dotenv

# Load .env file variables
load_dotenv()

class Settings:
    # --- App ---
    PROJECT_NAME: str = "Customer Support RAG API"
    VERSION: str = "0.1.0"
    DEBUG: bool = True

    # --- MongoDB ---
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "customer_support_rag")

    # --- Vector Database (Pinecone example) ---
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "")

    # --- LLM / Embeddings ---
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # --- Sentiment Model ---
    SENTIMENT_MODEL: str = os.getenv("SENTIMENT_MODEL", "distilbert-base-uncased-finetuned-sst-2-english")

    # --- Other Config ---
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")

settings = Settings()
