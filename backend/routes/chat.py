from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging

# --- Service Imports ---
from services import rag_services, sentiment_service, escalation_service, article_service
from db import mongo_client

router = APIRouter()

# (Schemas are unchanged)
# ---------- Schemas ----------
class MessageIn(BaseModel):
    customer_id: Optional[str] = None
    session_id: Optional[str] = None
    text: str
    top_k: int = 5
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


# ---------- Routes ----------
@router.post("/respond", response_model=ChatResponse)
async def respond(payload: MessageIn):
    session_id = payload.session_id or f"sess_{datetime.utcnow().timestamp()}"
    created_at = datetime.utcnow()

    try:
        # --- THIS IS OUR TEST ---
        # We will look for this exact message in the terminal.
        print("--- RUNNING THE NEW VERSION OF CHAT.PY ---")
        
        # This is the line with the 'await' fix.
        chunks = await article_service.search_articles(payload.text, payload.top_k)
        results = [Source(**chunk) for chunk in chunks]

        # (The rest of the function is the same)
        sentiment = await sentiment_service.analyze(payload.text)
        escalation = await escalation_service.predict(payload.text)
        reply_text = await rag_services.generate_answer(
            query=payload.text,
            sources=[s.dict() for s in results],
            sentiment=sentiment,
            tone=payload.preferred_tone
        )
        
        return ChatResponse(
            session_id=session_id,
            reply=reply_text,
            sentiment=sentiment,
            escalation=escalation,
            sources=results,
            created_at=created_at,
        )

    except Exception as e:
        logging.error(f"An exception occurred in /chat/respond: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

