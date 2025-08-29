from sqlalchemy import Column, String, JSON
from app.db import Base

class WorkflowDB(Base):
    __tablename__ = "pdf_workflows"

    workflow_id = Column(String, primary_key=True, index=True)
    state = Column(JSON, nullable=False)  # stores PDFState dict as JSON
