from langchain_community.vectorstores import Chroma
from app.models.state import PDFChatState
from langchain_huggingface import HuggingFaceEmbeddings
import os
os.environ['HF_HOME'] = 'C:/Users/Aditya/Desktop/Langchain/Langchain_Models/LOCALINSTALLEDMODELS'
embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

PERSIST_DIR = "./chroma_persist"
CHROMA_COLLECTION_NAME = "pdf_docs"

def embed_pdf_node(state: PDFChatState) -> PDFChatState:
    """
    Node: Embed PDF chunks into ChromaDB.
    Input: splitted_text
    Updates: vectordb_path, vectordb_collection
    """

    splitted_text = state.get("splitted_text", [])
    if not splitted_text:
        raise ValueError("No splitted_text found in state. Did you run split_pdf_node first?")

    # Create or load Chroma index
    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        vectordb = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embedding_model,
            collection_name=CHROMA_COLLECTION_NAME
        )
    else:
        vectordb = Chroma.from_documents(
            splitted_text,
            embedding_model,
            persist_directory=PERSIST_DIR,
            collection_name=CHROMA_COLLECTION_NAME
        )
        vectordb.persist()

    # Instead of storing `vectordb`, store its config
    state.update({
        "vectordb_path": PERSIST_DIR,
        "vectordb_collection": CHROMA_COLLECTION_NAME
    })

    return state
