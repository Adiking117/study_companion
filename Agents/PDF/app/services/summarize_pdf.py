from app.models.state import PDFChatState
from app.dependencies import get_chat_model

chat_model = get_chat_model()

def summarize_text_node(state: PDFChatState) -> PDFChatState:
    """
    Node: Summarize the entire PDF text.
    Input: extracted_text
    Updates: answer
    """

    extracted_text = state.get("extracted_text", "")

    if not extracted_text:
        raise ValueError("No extracted_text found in state. Did you run extract_text_node first?")

    # Build prompt
    prompt = f"Summarize the following content in detail:\n\n{extracted_text}"

    # Call LLM
    summary = chat_model.invoke(prompt).content

    # Update state
    state.update({
        "answer": summary # type: ignore
    }) # type: ignore

    return state
