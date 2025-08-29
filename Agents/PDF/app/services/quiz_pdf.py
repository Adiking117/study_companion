from app.models.state import PDFChatState
from app.dependencies import get_chat_model

chat_model = get_chat_model()

def generate_quiz_node(state: PDFChatState) -> PDFChatState:
    """
    Node: Generate a 10-question quiz for the entire PDF.
    Input: extracted_text
    Updates: answer
    """

    extracted_text = state.get("extracted_text", "")

    if not extracted_text:
        raise ValueError("No extracted_text found in state. Did you run extract_text_node first?")

    # Build prompt
    prompt = (
        "Based on the following content, create a quiz of 10 questions "
        "with answers at the end:\n\n"
        f"{extracted_text}"
    )

    # Call LLM
    quiz = chat_model.invoke(prompt).content

    # Update state
    state.update({
        "answer": quiz # type: ignore
    }) # type: ignore

    return state
