from app.models.state import PDFChatState
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
os.environ['HF_HOME'] = 'C:/Users/Aditya/Desktop/Langchain/Langchain_Models/LOCALINSTALLEDMODELS'

# Reuse the same embedding model as embed_pdf_node
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
def get_similar_pages_node(state: PDFChatState) -> PDFChatState:
    """
    Node: Retrieve similar pages from vectordb based on userQuery.
    Inputs: userQuery, vectordb_path, vectordb_collection
    Updates: similar_pages, similar_pages_content
    """
    userQuery = state.get("userQuery", "")
    vectordb_path = state.get("vectordb_path")
    vectordb_collection = state.get("vectordb_collection")

    if not userQuery:
        raise ValueError("No userQuery found in state.")
    if not vectordb_path or not vectordb_collection:
        raise ValueError("No vectordb config found in state. Did you run embed_pdf_node first?")

    vectordb = Chroma(
        persist_directory=vectordb_path,
        embedding_function=embedding_model,
        collection_name=vectordb_collection
    )

    # Retrieve documents
    retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 5})
    similar_pages = retriever.get_relevant_documents(userQuery)

    # Combine text
    similar_pages_content = "\n\n".join([doc.page_content for doc in similar_pages])

    state.update({
        "similar_pages": [doc.dict() for doc in similar_pages],  # make serializable
        "similar_pages_content": similar_pages_content
    })

    return state
