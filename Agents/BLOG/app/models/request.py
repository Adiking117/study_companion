from pydantic import BaseModel, HttpUrl
from typing import Optional

class BlogInput(BaseModel):
    """
    Input schema for triggering the workflow.
    """
    text: str  # YouTube link OR custom topic
    image_url: Optional[HttpUrl] = None  # Optional (Instagram posts)
