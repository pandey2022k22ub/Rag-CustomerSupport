# # from fastapi import FastAPI
# # from fastapi.middleware.cors import CORSMiddleware
# # from dotenv import load_dotenv

# # # Load environment variables
# # load_dotenv()

# # # Create FastAPI app
# # app = FastAPI(title="NerveSpark Backend")

# # # Enable CORS
# # app.add_middleware(
# #     CORSMiddleware,
# #     origins = [
# #     "http://localhost:3000",
# #     "http://127.0.0.1:3000"
# # ],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Import routes
# # from routes import articles, chat, escalation, feedback, sentiment

# # # Include routers
# # app.include_router(articles.router, prefix="/articles", tags=["Articles"])
# # app.include_router(chat.router, prefix="/chat", tags=["Chat"])
# # app.include_router(escalation.router, prefix="/escalation", tags=["Escalation"])
# # app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
# # app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment"])

# # # Health check
# # @app.get("/health")
# # def health_check():
# #     return {"status": "ok"}


# # backend/main.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(
#     title="RAG + Sentiment + Escalation backend (FastAPI)",
#     version="1.0.0",
#     description="Backend service for chatbot, sentiment analysis, articles, escalation, and feedback."
# )

# # CORS Middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000"
# ],  # Change to frontend domain in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Health check routes
# @app.get("/", tags=["system"])
# def root():
#     return {
#         "status": "ok",
#         "service": "Chatbot Backend",
#         "version": "1.0.0"
#     }

# @app.get("/health", tags=["system"])
# def health():
#     return {"status": "healthy"}

# # Import routers
# from routes import chat, sentiment, articles, escalation, feedback
# app.include_router(chat.router, prefix="/chat", tags=["Chat"])
# app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment"])
# app.include_router(articles.router, prefix="/articles", tags=["Articles"])
# app.include_router(escalation.router, prefix="/escalation", tags=["Escalation"])
# app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])

#/////////////////-------------------------------------2222222222222222222222222222222222222
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import logging

# # --- FastAPI App Initialization ---
# # Using the descriptive title and version from your app/main.py
# app = FastAPI(
#     title="Customer Support RAG API",
#     version="0.1.0",
#     description="RAG + Sentiment + Escalation backend (FastAPI)."
# )

# # --- CORS (Cross-Origin Resource Sharing) Middleware ---
# # Using the specific origins from your old backend/main.py for security.
# # This allows your React frontend at http://localhost:3000 to connect.
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#         "http://127.0.0.1:3000"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
#     allow_headers=["*"],  # Allows all headers
# )

# # --- Health and Root Endpoints ---
# # These are useful for checking if the server is running correctly.
# @app.get("/", tags=["System"])
# def root():
#     """Root endpoint to confirm the service is running."""
#     return {"status": "ok", "service": "customer-support-rag", "version": "0.1.0"}

# @app.get("/health", tags=["System"])
# def health():
#     """Health check endpoint."""
#     return {"status": "healthy"}

# # --- API Router Includes ---
# # This section imports and includes all your different API route modules.
# # The imports are now correct because this main.py file is in the `backend`
# # directory, which is the parent of the `routes` directory.
# try:
#     from routes import articles, chat, escalation, feedback, sentiment

#     app.include_router(articles.router, prefix="/articles", tags=["Articles"])
#     app.include_router(chat.router, prefix="/chat", tags=["Chat"])
#     app.include_router(escalation.router, prefix="/escalation", tags=["Escalation"])
#     app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
#     app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment"])

#     logging.info("All API routers loaded successfully.")

# except ImportError as e:
#     # This error will show in the console if a route file is missing.
#     logging.error(f"Could not import routes. Please ensure all route files exist. Error: {e}")

  #////////////////////////-------------------------3333333333333333333333333333333

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the centralized settings from your new config.py file
from config import settings

# --- Configure Logging ---
# This helps in seeing detailed logs in your terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Customer Support RAG API",
    version="0.1.0",
)

# --- CRITICAL: Verify CORS Origins ---
# This print statement will show in your terminal and confirm
# that the origins are being loaded correctly from your .env file.
logger.info(f"CORS: Allowing origins: {settings.ALLOWED_ORIGINS}")


# --- CORS Middleware ---
# This is the security policy that allows your frontend to connect.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# --- Health and Root Endpoints ---
@app.get("/", tags=["System"])
def root():
    return {"status": "ok", "service": "customer-support-rag"}

# --- API Router Includes ---
# We import the routers here to ensure the app is configured first
try:
    from routes import chat, sentiment, articles, escalation, feedback
    app.include_router(chat.router, prefix="/chat", tags=["Chat"])
    app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment"])
    app.include_router(articles.router, prefix="/articles", tags=["Articles"])
    app.include_router(escalation.router, prefix="/escalation", tags=["Escalation"])
    app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
    logger.info("All API routers loaded successfully.")
except ImportError as e:
    logger.error(f"Failed to import or include routers: {e}", exc_info=True)
