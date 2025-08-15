# services/article_service.py
from config.db import knowledge_base_collection
from utils.embedding_utils import get_embeddings
from bson import ObjectId

def add_article(title: str, content: str):
    """Add a new article with embeddings for retrieval."""
    embedding = get_embeddings(content)
    article_doc = {
        "title": title,
        "content": content,
        "embedding": embedding
    }
    result = knowledge_base_collection.insert_one(article_doc)
    return {"message": "Article added successfully", "id": str(result.inserted_id)}

def search_articles(query: str, top_k: int = 3):
    """Search articles using embeddings similarity."""
    query_embedding = get_embeddings(query)

    # Simple cosine similarity search (if using MongoDB vector search plugin or external DB)
    # Here: retrieving all and scoring manually (for demo)
    all_articles = list(knowledge_base_collection.find({}))
    scored = []
    for art in all_articles:
        score = cosine_similarity(query_embedding, art["embedding"])
        scored.append((art, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    top_articles = [a[0] for a in scored[:top_k]]

    return [{"title": a["title"], "content": a["content"]} for a in top_articles]

def cosine_similarity(vec1, vec2):
    """Basic cosine similarity."""
    import numpy as np
    v1, v2 = np.array(vec1), np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
