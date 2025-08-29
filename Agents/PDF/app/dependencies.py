from app.config import settings
from langchain_groq import ChatGroq

def get_chat_model():
    """Provides a singleton ChatGroq model instance."""
    return ChatGroq(model="llama3-8b-8192")
    # return ChatGroq(model="openai/gpt-oss-120b")
