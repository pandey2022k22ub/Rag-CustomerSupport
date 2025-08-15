# app/routes/sentiment.py
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# --- Optional service import ---
_sentiment = None
try:
    from app.services import sentiment_service as _sentiment  # type: ignore
except Exception:
    _sentiment = None


class SentimentIn(BaseModel):
    text: str


class SentimentOut(BaseModel):
    label: str
    score: float
    emotions: Optional[dict] = None


class SentimentBatchIn(BaseModel):
    texts: List[str]


class SentimentBatchOut(BaseModel):
    results: List[SentimentOut]


def _fallback_analyze(text: str) -> SentimentOut:
    t = text.lower()
    if any(w in t for w in ["angry", "furious", "hate", "useless", "worst", "terrible"]):
        return SentimentOut(label="very_negative", score=0.95, emotions={"anger": 0.9})
    if any(w in t for w in ["not happy", "bad", "issue", "problem", "can't", "cannot", "delay"]):
        return SentimentOut(label="negative", score=0.75, emotions={"sadness": 0.6})
    if any(w in t for w in ["great", "thanks", "love", "awesome", "perfect", "resolved"]):
        return SentimentOut(label="positive", score=0.9, emotions={"joy": 0.85})
    return SentimentOut(label="neutral", score=0.6, emotions={"neutral": 0.7})


@router.post("/analyze", response_model=SentimentOut)
async def analyze(payload: SentimentIn):
    """
    Run sentiment/emotion analysis on a single text message.
    """
    if _sentiment and hasattr(_sentiment, "analyze"):
        return await _sentiment.analyze(payload.text)  # type: ignore
    return _fallback_analyze(payload.text)


@router.post("/batch", response_model=SentimentBatchOut)
async def batch(payload: SentimentBatchIn):
    """
    Run batch sentiment on multiple texts.
    """
    if _sentiment and hasattr(_sentiment, "batch_analyze"):
        results = await _sentiment.batch_analyze(payload.texts)  # type: ignore
        # Ensure schema compatibility
        normalized = [
            SentimentOut(label=r.get("label", "neutral"), score=float(r.get("score", 0.5)), emotions=r.get("emotions"))
            for r in results
        ]
        return SentimentBatchOut(results=normalized)

    # Fallback
    return SentimentBatchOut(results=[_fallback_analyze(t) for t in payload.texts])
