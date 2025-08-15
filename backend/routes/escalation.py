# app/routes/escalation.py
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# --- Optional service import ---
_escalation = None
try:
    from app.services import escalation_service as _escalation  # type: ignore
except Exception:
    _escalation = None

# --- Simple rules for fallback ---
_DEFAULT_RULES = [
    "refund", "chargeback", "legal", "lawsuit",
    "complaint", "escalate", "supervisor", "manager",
    "cancel my account", "switch provider"
]


class EscalationIn(BaseModel):
    text: str
    history: Optional[List[str]] = None


class EscalationOut(BaseModel):
    predicted: bool
    score: float
    reasons: List[str]


@router.get("/rules", response_model=List[str])
async def rules():
    """
    Returns baseline escalation trigger phrases.
    """
    if _escalation and hasattr(_escalation, "rules"):
        try:
            return await _escalation.rules()  # type: ignore
        except Exception:
            pass
    return _DEFAULT_RULES


@router.post("/predict", response_model=EscalationOut)
async def predict(payload: EscalationIn):
    """
    Predict whether a message (optionally with history) should be escalated.
    """
    if _escalation and hasattr(_escalation, "predict"):
        return await _escalation.predict(payload.text, payload.history)  # type: ignore

    # Fallback: keyword match
    txt = payload.text.lower()
    hits = [k for k in _DEFAULT_RULES if k in txt]
    score = 0.0
    if hits:
        score = 0.85 + 0.03 * min(5, len(hits))
    return EscalationOut(predicted=score >= 0.88, score=round(score, 2), reasons=hits)
