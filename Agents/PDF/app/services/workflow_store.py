from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models.workflow_db import WorkflowDB
from app.models.state import PDFChatState
from langchain_core.documents import Document
import uuid


# --- Create tables ---
WorkflowDB.metadata.create_all(bind=engine)


# --- DB Session Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Serialization Helpers ---
def _serialize_state(state: PDFChatState) -> dict:
    """Convert Documents inside state into JSON-serializable dicts."""
    serializable_state = {}
    for key, value in state.items():
        if isinstance(value, Document):
            serializable_state[key] = value.dict()
        elif isinstance(value, list):
            new_list = []
            for item in value:
                if isinstance(item, Document):
                    new_list.append(item.dict())
                else:
                    new_list.append(item)
            serializable_state[key] = new_list
        elif key == "vectordb":
            # Don't store raw Chroma object, just path + collection
            serializable_state["vectordb_path"] = state.get("vectordb_path")
            serializable_state["vectordb_collection"] = state.get("vectordb_collection")
        else:
            serializable_state[key] = value
    return serializable_state


def _deserialize_state(state: dict) -> PDFChatState:
    """Rebuild Documents from dicts where applicable."""
    deserialized_state: PDFChatState = {}
    for key, value in state.items():
        if isinstance(value, dict) and "page_content" in value:
            deserialized_state[key] = Document(**value)
        elif isinstance(value, list):
            new_list = []
            for item in value:
                if isinstance(item, dict) and "page_content" in item:
                    new_list.append(Document(**item))
                else:
                    new_list.append(item)
            deserialized_state[key] = new_list
        else:
            deserialized_state[key] = value
    return deserialized_state  # type: ignore


# --- CRUD Operations ---
def create_workflow(db: Session, initial_state: PDFChatState, workflow_id: str | None = None) -> str:
    if workflow_id is None:
        workflow_id = str(uuid.uuid4())
    db_obj = WorkflowDB(
        workflow_id=workflow_id,
        state=_serialize_state(initial_state)
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return workflow_id


def get_workflow(db: Session, workflow_id: str) -> PDFChatState | None:
    wf = db.query(WorkflowDB).filter(WorkflowDB.workflow_id == workflow_id).first()
    if not wf:
        return None
    return _deserialize_state(wf.state)  # type: ignore


def update_workflow(db: Session, workflow_id: str, state: PDFChatState) -> PDFChatState | None:
    wf = db.query(WorkflowDB).filter(WorkflowDB.workflow_id == workflow_id).first()
    if not wf:
        return None
    wf.state = _serialize_state(state)
    db.commit()
    db.refresh(wf)
    return _deserialize_state(wf.state)  # type: ignore
