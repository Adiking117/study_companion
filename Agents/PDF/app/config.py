import os
from dotenv import load_dotenv

load_dotenv()  # load .env file

class Settings:
    # Groq / LLM
    GROQ_MODEL: str = os.getenv("GROQ_API_KEY") # type: ignore

    # App
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = APP_ENV == "development"

settings = Settings()
