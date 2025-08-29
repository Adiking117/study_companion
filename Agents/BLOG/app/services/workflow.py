from typing import Dict
from app.models.state import BlogState
from app.workflows.blog_workflow import build_blog_workflow
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.sqlite import SqliteSaver

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

# Open SQLite connection
conn = sqlite3.connect("blog_workflows.db", check_same_thread=False)

# Pass connection to SqliteSaver
checkpointer = SqliteSaver(conn)

# Compile with checkpointer
_blog_workflow = build_blog_workflow().compile(checkpointer=checkpointer)


def run_blog_workflow(state: BlogState, workflow_id: str) -> Dict:
    try:
        return _blog_workflow.invoke(
            state,
            config={"configurable": {"thread_id": workflow_id}},
        )
    except RuntimeError as e:
        if "PAUSE" in str(e):
            return state # type: ignore
        raise
