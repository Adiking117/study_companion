from typing import Dict
import sqlite3
from app.models.state import PDFChatState
from app.workflows.pdf_workflow import build_pdf_workflow
from langgraph.checkpoint.sqlite import SqliteSaver

# Open SQLite connection (safe for multi-thread, but not multi-process)
conn = sqlite3.connect("pdf_workflows.db", check_same_thread=False)

# Initialize checkpointer
checkpointer = SqliteSaver(conn)

# Compile workflow with persistence
_pdf_workflow = build_pdf_workflow().compile(checkpointer=checkpointer)

def run_blog_workflow(state: PDFChatState, workflow_id: str) -> PDFChatState:
    """
    Run the PDF workflow with checkpointing.
    Resumes if workflow_id exists, otherwise starts new.
    Handles HITL pauses gracefully.
    """
    try:
        return _pdf_workflow.invoke(
            state,
            config={"configurable": {"thread_id": workflow_id}},
        )  # type: ignore
    except RuntimeError as e:
        # LangGraph PAUSE (HITL)
        if "PAUSE" in str(e):
            return state
        raise
