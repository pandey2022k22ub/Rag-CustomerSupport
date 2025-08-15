# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# app/main.py



app = FastAPI(
    title="Customer Support RAG API",
    version="0.1.0",
    description="RAG + Sentiment + Escalation backend (FastAPI)."
)

# --- CORS (adjust origins if you know your frontend URL) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # e.g., ["https://your-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health & root endpoints ---   
@app.get("/", tags=["system"])
def root():
    return {"status": "ok", "service": "customer-support-rag", "version": "0.1.0"}

@app.get("/health", tags=["system"])
def health():
    return {"status": "healthy"}

# --- Router includes (safe to run before files exist) ---
def _include_routers():
    """
    Import routers lazily so main.py can start even if route files
    aren’t created yet. When you add each route file, just restart.
    """
    try:
        from app.routes import chat, sentiment, articles, escalation, feedback
        app.include_router(chat.router, prefix="/chat", tags=["chat"])
        app.include_router(sentiment.router, prefix="/sentiment", tags=["sentiment"])
        app.include_router(articles.router, prefix="/articles", tags=["articles"])
        app.include_router(escalation.router, prefix="/escalation", tags=["escalation"])
        app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
    except Exception as e:
        # During first boots (before files exist) this is expected.
        # Print to console for visibility; app still runs.
        print(f"[main] Routers not fully loaded yet: {e}")

_include_routers()
