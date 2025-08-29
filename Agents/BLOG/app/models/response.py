from pydantic import BaseModel
from typing import Optional, Dict, Any

class BlogResponse(BaseModel):
    status: str
    data: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    message: str

class ErrorResponse(BaseModel):
    detail: str
