# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Create FastAPI app
# app = FastAPI(title="NerveSpark Backend")

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     origins = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000"
# ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Import routes
# from routes import articles, chat, escalation, feedback, sentiment

# # Include routers
# app.include_router(articles.router, prefix="/articles", tags=["Articles"])
# app.include_router(chat.router, prefix="/chat", tags=["Chat"])
# app.include_router(escalation.router, prefix="/escalation", tags=["Escalation"])
# app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
# app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment"])

# # Health check
# @app.get("/health")
# def health_check():
#     return {"status": "ok"}


# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RAG + Sentiment + Escalation backend (FastAPI)",
    version="1.0.0",
    description="Backend service for chatbot, sentiment analysis, articles, escalation, and feedback."
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
],  # Change to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check routes
@app.get("/", tags=["system"])
def root():
    return {
        "status": "ok",
        "service": "Chatbot Backend",
        "version": "1.0.0"
    }

@app.get("/health", tags=["system"])
def health():
    return {"status": "healthy"}

# Import routers
from routes import chat, sentiment, articles, escalation, feedback
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment"])
app.include_router(articles.router, prefix="/articles", tags=["Articles"])
app.include_router(escalation.router, prefix="/escalation", tags=["Escalation"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
