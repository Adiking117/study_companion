from pydantic import BaseModel, HttpUrl
from typing import Optional

class PDFInput(BaseModel):
    """
    Input schema for triggering the workflow.
    """
    userquery: str
    pdf_path: str
