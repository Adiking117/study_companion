from langgraph.graph import StateGraph, END

from app.models.state import PDFChatState
from app.services.answer_question import answer_question_on_query_node
from app.services.embed_pdf import embed_pdf_node
from app.services.extract_text import extract_text_node
from app.services.pdf_load import load_pdf_node
from app.services.quiz_pdf import generate_quiz_node
from app.services.quiz_topic import generate_quiz_on_topic_node
from app.services.similar_pages import get_similar_pages_node
from app.services.split_pdf import split_pdf_node
from app.services.summarize_pdf import summarize_text_node
from app.services.summarize_topic import summarize_on_topic_node



# --- Router functions ---
def first_router(state: PDFChatState):
    """Route based on whether query is PDF-level or retrieval-level."""
    category = state["userQueryCategory"]
    if category in ["summpdf", "quizpdf"]:
        return "extract_text"
    else:
        return "split_pdf"

def second_router(state: PDFChatState):
    """Route retrieval-based queries to the correct node."""
    category = state["userQueryCategory"]
    if category == "qa":
        return "answer_question_on_query"
    elif category == "summtopic":
        return "summarize_on_topic"
    elif category == "quiztopic":
        return "generate_quiz_on_topic"
    else:
        raise ValueError(f"Invalid category for retrieval path: {category}")

def pdf_router(state: PDFChatState):
    """Route PDF-level queries to the correct node."""
    category = state["userQueryCategory"]
    if category == "summpdf":
        return "summarize_text"
    elif category == "quizpdf":
        return "generate_quiz"
    else:
        raise ValueError(f"Invalid category for PDF path: {category}")




def build_pdf_workflow():
    
    workflow = StateGraph(PDFChatState)

    # --- Add Nodes ---
    workflow.add_node("load_pdf", load_pdf_node)
    workflow.add_node("extract_text", extract_text_node)
    workflow.add_node("split_pdf", split_pdf_node)
    workflow.add_node("embed_pdf", embed_pdf_node)
    workflow.add_node("get_similar_pages", get_similar_pages_node)

    workflow.add_node("answer_question_on_query", answer_question_on_query_node)
    workflow.add_node("summarize_on_topic", summarize_on_topic_node)
    workflow.add_node("generate_quiz_on_topic", generate_quiz_on_topic_node)
    workflow.add_node("summarize_text", summarize_text_node)
    workflow.add_node("generate_quiz", generate_quiz_node)



    # --- Edges ---
    workflow.set_entry_point("load_pdf")

    # First branching
    workflow.add_conditional_edges(
        "load_pdf",
        first_router,
        {
            "extract_text": "extract_text",
            "split_pdf": "split_pdf"
        }
    )

    # PDF path
    workflow.add_conditional_edges(
        "extract_text",
        pdf_router,
        {
            "summarize_text": "summarize_text",
            "generate_quiz": "generate_quiz"
        }
    )
    workflow.add_edge("summarize_text", END)
    workflow.add_edge("generate_quiz", END)

    # Retrieval path
    workflow.add_edge("split_pdf", "embed_pdf")
    workflow.add_edge("embed_pdf", "get_similar_pages")

    workflow.add_conditional_edges(
        "get_similar_pages",
        second_router,
        {
            "answer_question_on_query": "answer_question_on_query",
            "summarize_on_topic": "summarize_on_topic",
            "generate_quiz_on_topic": "generate_quiz_on_topic"
        }
    )

    workflow.add_edge("answer_question_on_query", END)
    workflow.add_edge("summarize_on_topic", END)
    workflow.add_edge("generate_quiz_on_topic", END)

    # --- Compile graph ---
    # app = workflow.compile()

    # return app

    return workflow



