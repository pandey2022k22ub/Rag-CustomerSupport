# app/routes/chat.py
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# --- Optional service imports (graceful fallback if missing) ---
_rag = _sent = _esc = _articles = _db = None
try:
    from app.services import rag_service as _rag  # type: ignore
except Exception:
    _rag = None
try:
    from app.services import sentiment_service as _sent  # type: ignore
except Exception:
    _sent = None
try:
    from app.services import escalation_service as _esc  # type: ignore
except Exception:
    _esc = None
try:
    from app.services import article_service as _articles  # type: ignore
except Exception:
    _articles = None
try:
    from app.db import mongo_client as _db  # type: ignore
except Exception:
    _db = None


# ---------- Schemas ----------
class MessageIn(BaseModel):
    customer_id: Optional[str] = None
    session_id: Optional[str] = None
    text: str
    top_k: int = 5
    # You can pass UI hints if needed
    preferred_tone: Optional[str] = None
    metadata: Optional[dict] = None


class Source(BaseModel):
    id: str
    title: Optional[str] = None
    snippet: Optional[str] = None
    score: Optional[float] = None
    url: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    sentiment: Optional[dict] = None
    escalation: Optional[dict] = None
    sources: List[Source] = []
    created_at: datetime


# ---------- Helpers ----------
def _fallback_sentiment(text: str) -> dict:
    txt = text.lower()
    if any(w in txt for w in ["angry", "furious", "hate", "useless", "worst", "cancel"]):
        return {"label": "very_negative", "score": 0.95}
    if any(w in txt for w in ["not happy", "bad", "issue", "problem", "can't", "cannot"]):
        return {"label": "negative", "score": 0.75}
    if any(w in txt for w in ["great", "thanks", "love", "awesome", "perfect"]):
        return {"label": "positive", "score": 0.9}
    return {"label": "neutral", "score": 0.6}


def _fallback_escalation(text: str) -> dict:
    txt = text.lower()
    triggers = ["refund", "chargeback", "sue", "legal", "complaint", "manager", "escalate"]
    score = 0.0
    hits = [t for t in triggers if t in txt]
    if hits:
        score = 0.8 + 0.05 * min(3, len(hits))
    return {"predicted": score >= 0.85, "score": round(score, 2), "reasons": hits}


# ---------- Routes ----------
@router.post("/respond", response_model=ChatResponse)
async def respond(payload: MessageIn):
    """
    Main chat endpoint:
      1) Retrieve relevant KB chunks
      2) Analyze sentiment
      3) Predict escalation
      4) Generate empathetic response using RAG
      5) Log to DB (if available)
    """
    session_id = payload.session_id or f"sess_{datetime.utcnow().timestamp()}"
    created_at = datetime.utcnow()

    # Retrieve context
    results = []
    if _articles and hasattr(_articles, "search_articles"):
        chunks = await _articles.search_articles(payload.text, payload.top_k)  # type: ignore
        for c in chunks:
            results.append(
                Source(
                    id=str(c.get("id", "")),
                    title=c.get("metadata", {}).get("title"),
                    snippet=c.get("text", "")[:240],
                    score=float(c.get("score", 0)),
                    url=c.get("metadata", {}).get("url"),
                )
            )
    else:
        results = [
            Source(
                id="fallback_1",
                title="No KB connected",
                snippet="Set up vector DB to enable retrieval.",
                score=0.42,
                url=None,
            )
        ]

    # Sentiment
    if _sent and hasattr(_sent, "analyze"):
        sentiment = await _sent.analyze(payload.text)  # type: ignore
    else:
        sentiment = _fallback_sentiment(payload.text)

    # Escalation
    if _esc and hasattr(_esc, "predict"):
        escalation = await _esc.predict(payload.text, history=None)  # type: ignore
    else:
        escalation = _fallback_escalation(payload.text)

    # RAG answer
    if _rag and hasattr(_rag, "generate_answer"):
        reply_text = await _rag.generate_answer(query=payload.text, sources=[s.dict() for s in results], sentiment=sentiment, tone=payload.preferred_tone)  # type: ignore
    else:
        # Empathy shim in fallback
        prefix = ""
        if sentiment["label"].startswith("neg"):
            prefix = "I'm sorry you're facing this. "
        elif sentiment["label"].startswith("very_"):
            prefix = "I truly understand this is frustrating. "
        reply_text = (
            f"{prefix}Here’s what I can suggest based on our help center: "
            f"{results[0].snippet if results else 'please connect your knowledge base.'}"
        )

    # Log conversation if DB is present
    if _db and hasattr(_db, "get_db"):
        try:
            db = _db.get_db()
            db.chat_sessions.update_one(
                {"session_id": session_id},
                {
                    "$setOnInsert": {
                        "session_id": session_id,
                        "customer_id": payload.customer_id,
                        "created_at": created_at,
                    },
                    "$push": {
                        "messages": {
                            "sender": "customer",
                            "text": payload.text,
                            "timestamp": created_at,
                            "sentiment": sentiment,
                        }
                    },
                    "$set": {"updated_at": datetime.utcnow()},
                },
                upsert=True,
            )
            db.chat_sessions.update_one(
                {"session_id": session_id},
                {
                    "$push": {
                        "messages": {
                            "sender": "bot",
                            "text": reply_text,
                            "timestamp": datetime.utcnow(),
                        }
                    }
                },
            )
        except Exception as e:
            print(f"[chat.respond] DB log skipped: {e}")

    return ChatResponse(
        session_id=session_id,
        reply=reply_text,
        sentiment=sentiment,
        escalation=escalation,
        sources=results,
        created_at=created_at,
    )
