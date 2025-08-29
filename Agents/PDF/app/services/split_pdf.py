from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.models.state import PDFChatState

def split_pdf_node(state: PDFChatState) -> PDFChatState:
    """
    Node: Split PDF into smaller chunks.
    Input: pdf
    Updates: splitted_text
    """

    pdf = state.get("pdf", [])

    if not pdf:
        raise ValueError("No PDF content found in state. Did you run load_pdf_node first?")

    # Split PDF
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    splitted_text = splitter.split_documents(pdf)

    # Update state
    state.update({
        "splitted_text": splitted_text
    })

    return state
