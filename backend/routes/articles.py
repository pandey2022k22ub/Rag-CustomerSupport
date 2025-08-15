# app/routes/articles.py
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, HttpUrl
from datetime import datetime

router = APIRouter()

# --- Optional service imports (graceful fallback if missing) ---
_article_service = None
try:
    from app.services import article_service as _article_service  # type: ignore
except Exception:
    _article_service = None


# ---------- Schemas ----------
class ArticleIn(BaseModel):
    title: str
    content: str
    source: Optional[str] = None
    url: Optional[HttpUrl] = None
    tags: Optional[List[str]] = None
    created_at: Optional[datetime] = None


class IngestResponse(BaseModel):
    ingested: int
    details: Optional[List[str]] = None


class RetrievedChunk(BaseModel):
    id: str
    score: float
    text: str
    metadata: dict


class SearchResponse(BaseModel):
    query: str
    top_k: int
    results: List[RetrievedChunk]


# ---------- Routes ----------
@router.post("/ingest", response_model=IngestResponse)
async def ingest_articles(payload: List[ArticleIn]):
    """
    Ingest raw help articles. If a service is present, it will:
      1) chunk -> embed -> upsert to vector DB
      2) store raw docs/meta in Mongo (optional)
    Fallback: return a mock success without doing anything.
    """
    if _article_service and hasattr(_article_service, "ingest_articles"):
        count, details = await _article_service.ingest_articles([a.dict() for a in payload])  # type: ignore
        return IngestResponse(ingested=count, details=details)

    # Fallback
    return IngestResponse(ingested=len(payload), details=["(fallback) no article_service found"])


@router.get("/search", response_model=SearchResponse)
async def search_articles(
    q: str = Query(..., description="Customer query to search relevant KB chunks"),
    top_k: int = Query(5, ge=1, le=20)
):
    """
    Semantic search over knowledge base (vector DB).
    """
    if _article_service and hasattr(_article_service, "search_articles"):
        chunks = await _article_service.search_articles(q, top_k)  # type: ignore
        results = [
            RetrievedChunk(
                id=c.get("id", ""),
                score=float(c.get("score", 0)),
                text=c.get("text", ""),
                metadata=c.get("metadata", {}) or {},
            )
            for c in chunks
        ]
        return SearchResponse(query=q, top_k=top_k, results=results)

    # Fallback naive response
    return SearchResponse(
        query=q,
        top_k=top_k,
        results=[
            RetrievedChunk(
                id="fallback_1", score=0.42, text=f"(fallback) No vector DB configured for: {q}", metadata={}
            )
        ],
    )


@router.get("/{doc_id}")
async def get_article(doc_id: str):
    """
    Fetch a single stored article (raw) by ID from your DB (Mongo).
    """
    if _article_service and hasattr(_article_service, "get_article"):
        art = await _article_service.get_article(doc_id)  # type: ignore
        if not art:
            raise HTTPException(status_code=404, detail="Article not found")
        return art

    # Fallback
    if doc_id == "fallback_1":
        return {"id": doc_id, "title": "Fallback Doc", "content": "No DB connected.", "metadata": {}}
    raise HTTPException(status_code=404, detail="Article not found (fallback)")
