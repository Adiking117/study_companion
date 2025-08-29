from pydantic import BaseModel
from typing import Optional, Dict, Any

class PDFResponse(BaseModel):
    data: str

class HealthResponse(BaseModel):
    status: str
    message: str

class ErrorResponse(BaseModel):
    detail: str
