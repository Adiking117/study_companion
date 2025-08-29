from app.models.state import PDFChatState


def extract_text_node(state: PDFChatState) -> PDFChatState:
    """
    Node: Extract full text from loaded PDF.
    Input: pdf
    Updates: extracted_text
    """

    pdf = state.get("pdf", [])

    if not pdf:
        raise ValueError("No PDF content found in state. Did you run load_pdf_node first?")

    # Extract text
    full_text = "\n".join([doc.page_content for doc in pdf])

    # Update state
    state.update({
        "extracted_text": full_text
    })

    return state
