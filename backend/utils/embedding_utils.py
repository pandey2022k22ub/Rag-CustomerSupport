# backend/utils/embedding_utils.py
from sentence_transformers import SentenceTransformer
import logging

# Load the sentence transformer model. This will download the model the first time it's run.
# "all-MiniLM-L6-v2" is a good, lightweight default model.
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    logging.info("SentenceTransformer model 'all-MiniLM-L6-v2' loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load SentenceTransformer model: {e}")
    model = None

def get_embeddings(text: str) -> list[float]: # <--- RENAMED THIS FUNCTION
    """
    Generates an embedding for a given text using the loaded SentenceTransformer model.
    """
    if model is None:
        logging.error("Embedding model is not available.")
        return []
        
    # The model.encode() method creates the vector embedding
    embedding = model.encode(text, convert_to_tensor=False)
    return embedding.tolist()

