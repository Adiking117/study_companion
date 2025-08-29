from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models.workflow_db import WorkflowDB
from app.models.state import BlogState
import uuid

# Create tables
WorkflowDB.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_workflow(db: Session, initial_state: BlogState,workflow_id) -> str:
    # workflow_id = str(uuid.uuid4())
    db_obj = WorkflowDB(workflow_id=workflow_id, state=initial_state)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return workflow_id


def get_workflow(db: Session, workflow_id: str) -> BlogState | None:
    wf = db.query(WorkflowDB).filter(WorkflowDB.workflow_id == workflow_id).first()
    return wf.state if wf else None # type: ignore


def update_workflow(db: Session, workflow_id: str, state: dict):
    wf = db.query(WorkflowDB).filter(WorkflowDB.workflow_id == workflow_id).first()
    if not wf:
        return None
    wf.state = state # type: ignore
    db.commit()
    db.refresh(wf)
    return wf.state
