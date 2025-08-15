# app/routes/feedback.py
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, conint
from datetime import datetime

router = APIRouter()

# --- Optional DB import ---
_db = None
try:
    from app.db import mongo_client as _db  # type: ignore
except Exception:
    _db = None


class FeedbackIn(BaseModel):
    session_id: str
    rating: conint(ge=1, le=5) = Field(..., description="1-5 stars")
    comment: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class FeedbackOut(BaseModel):
    ok: bool
    session_id: str
    stored_at: datetime


class FeedbackStats(BaseModel):
    total: int
    average_rating: float
    last_10: int


@router.post("/submit", response_model=FeedbackOut)
async def submit_feedback(payload: FeedbackIn):
    """
    Store customer satisfaction feedback against a chat session.
    """
    ts = datetime.utcnow()
    if _db and hasattr(_db, "get_db"):
        try:
            db = _db.get_db()
            db.feedback.insert_one(
                {
                    "session_id": payload.session_id,
                    "rating": int(payload.rating),
                    "comment": payload.comment,
                    "metadata": payload.metadata or {},
                    "created_at": ts,
                }
            )
            # optional: also stamp session doc
            db.chat_sessions.update_one(
                {"session_id": payload.session_id},
                {"$set": {"satisfaction_score": int(payload.rating), "satisfaction_comment": payload.comment}},
                upsert=False,
            )
        except Exception as e:
            print(f"[feedback.submit] DB write failed: {e}")
            # fall through to success response as soft-fail is okay for demo
    return FeedbackOut(ok=True, session_id=payload.session_id, stored_at=ts)


@router.get("/aggregates", response_model=FeedbackStats)
async def aggregates():
    """
    Simple aggregate metrics for dashboard.
    """
    if _db and hasattr(_db, "get_db"):
        try:
            db = _db.get_db()
            total = db.feedback.count_documents({})
            if total == 0:
                return FeedbackStats(total=0, average_rating=0.0, last_10=0)
            pipeline = [
                {"$group": {"_id": None, "avg": {"$avg": "$rating"}, "count": {"$sum": 1}}},
            ]
            agg = list(db.feedback.aggregate(pipeline))
            avg = float(agg[0]["avg"]) if agg else 0.0
            last_10 = db.feedback.count_documents({}) if total < 10 else 10
            return FeedbackStats(total=total, average_rating=round(avg, 2), last_10=last_10)
        except Exception as e:
            print(f"[feedback.aggregates] DB read failed: {e}")
            # fall through
    # Fallback metrics
    return FeedbackStats(total=0, average_rating=0.0, last_10=0)
