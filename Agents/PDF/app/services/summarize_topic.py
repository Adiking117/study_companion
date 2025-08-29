from app.dependencies import get_chat_model
from app.models.state import PDFChatState

chat_model = get_chat_model()
def summarize_on_topic_node(state: PDFChatState) -> PDFChatState:
    """
    Node: Summarize a specific topic using retrieved similar pages.
    Inputs: similar_pages_content, userQuery (used as topic)
    Updates: answer
    """

    similar_pages_content = state.get("similar_pages_content", "")
    topic = state.get("userQuery", "")

    if not topic:
        raise ValueError("No topic (userQuery) found in state.")
    if not similar_pages_content:
        raise ValueError("No similar_pages_content found in state. Did you run get_similar_pages_node first?")

    # Build prompt
    prompt = (
        f"Summarize the following content in detail:\n\n"
        f"Topic: {topic}\n\n"
        f"Context:\n{similar_pages_content}\n\n"
        f"Also add your suggestions in the summary if there is lack of context."
    )

    # Call LLM
    summary = chat_model.invoke(prompt).content

    # Update state
    state.update({
        "answer": summary # type: ignore
    }) # type: ignore

    return state
