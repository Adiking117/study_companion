from app.models.state import PDFChatState

from app.dependencies import get_chat_model

chat_model = get_chat_model()

def generate_quiz_on_topic_node(state: PDFChatState) -> PDFChatState:
    """
    Node: Generate a 10-question quiz on a specific topic using retrieved similar pages.
    Inputs: similar_pages_content, userQuery
    Updates: answer
    """

    similar_pages_content = state.get("similar_pages_content", "")
    user_query = state.get("userQuery", "")

    if not user_query:
        raise ValueError("No userQuery found in state.")
    if not similar_pages_content:
        raise ValueError("No similar_pages_content found in state. Did you run get_similar_pages_node first?")

    # Build prompt
    prompt = (
        f"Based on the following content:\n{similar_pages_content}\n\n"
        f"Create a quiz of 10 questions with answers at the end "
        f"on the topic: {user_query}.\n\n"
        f"Also add your suggestions in the quiz if there is lack of context."
    )

    # Call LLM
    quiz = chat_model.invoke(prompt).content

    # Update state
    state.update({
        "answer": quiz # type: ignore
    }) # type: ignore

    return state
