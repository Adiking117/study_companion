from app.dependencies import get_chat_model
from app.models.state import PDFChatState

chat_model = get_chat_model()

def answer_question_on_query_node(state: PDFChatState) -> PDFChatState:
    """
    Node: Answer a question based on retrieved similar pages.
    Inputs: similar_pages_content, userQuery
    Updates: answer
    """

    similar_pages_content = state.get("similar_pages_content", "")
    user_query = state.get("userQuery", "")

    if not user_query:
        raise ValueError("No userQuery found in state.")
    if not similar_pages_content:
        raise ValueError("No similar_pages_content found in state. Did you run get_similar_pages_node first?")

    # Create prompt
    prompt = (
        f"Answer the question using the following context:\n\n"
        f"{similar_pages_content}\n\n"
        f"Question: {user_query}\n\n"
        f"Also add your suggestions in the answer if there is lack of context."
    )

    # Call LLM
    answer = chat_model.invoke(prompt).content

    # Update state
    state.update({
        "answer": answer # type: ignore
    }) # type: ignore

    return state
