from langchain_community.document_loaders import PyPDFLoader
import os

from app.models.state import PDFChatState
from app.services.classification_chain import get_classification_chain

# --- Node Function ---
def load_pdf_node(state: PDFChatState) -> PDFChatState:
    """
    Node: Loads PDF and classifies user query.
    Inputs: pdfpath, userQuery
    Updates: pdfpath, pdf, userQuery, userQueryCategory
    """

    pdfpath = state.get("pdfpath")
    userQuery = state.get("userQuery")

    # 1. Load PDF
    if not os.path.exists(pdfpath):
        raise FileNotFoundError(f"PDF file '{pdfpath}' not found.")

    loader = PyPDFLoader(pdfpath)
    pdf = loader.load()

    # 2. Classify userQuery into category using classification_chain
    userQueryCategory = get_classification_chain().invoke({"query": userQuery})

    # 3. Update state
    state.update({
        "pdfpath": pdfpath,
        "pdf": pdf,
        "userQuery": userQuery,
        "userQueryCategory": userQueryCategory.category
    })

    return state
