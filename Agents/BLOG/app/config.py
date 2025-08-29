import os
from dotenv import load_dotenv

load_dotenv()  # load .env file

class Settings:
    # Groq / LLM
    GROQ_MODEL: str = os.getenv("GROQ_API_KEY") # type: ignore

    # Facebook
    FACEBOOK_PAGE_ID: str = os.getenv("FACEBOOK_PAGE_ID", "")
    FACEBOOK_PAGE_TOKEN: str = os.getenv("FACEBOOK_PAGE_TOKEN", "")
    FACEBOOK_GRAPH_API_VERSION: str = os.getenv("FACEBOOK_GRAPH_API_VERSION", "v16.0")

    # Instagram
    INSTAGRAM_PAGE_ID: str = os.getenv("INSTAGRAM_PAGE_ID", "")

    # App
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = APP_ENV == "development"

settings = Settings()
