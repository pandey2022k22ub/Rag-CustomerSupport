import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

class Settings:
    # --- CORS Origins ---
    # Load origins from .env, with a fallback for development
    ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

    # --- Gemini API Key ---
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

    # You can add other settings here as your app grows
    # MONGODB_URI: str = os.getenv("MONGODB_URI")

# Create a single instance of the settings to be imported by other files
settings = Settings()