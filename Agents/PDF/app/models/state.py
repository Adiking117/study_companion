from typing import Any, TypedDict, Literal, Dict, List
import operator
from typing_extensions import Annotated
from langchain_community.vectorstores import Chroma
from typing import Any, TypedDict, Literal, List, Optional


class PDFChatState(TypedDict, total=False):
    pdfpath: str
    pdf: List[Any]   # list of Documents
    userQuery: str
    userQueryCategory: Literal["qa", "summpdf", "quizpdf", "summtopic", "quiztopic"]
    extracted_text: str
    splitted_text: List[Any]  # list of text chunks/documents
    vectordb_path: Optional[str]        # ✅ persist directory instead of Chroma object
    vectordb_collection: Optional[str]  # ✅ collection name reference
    similar_pages: List[Any]            # retrieved docs
    similar_pages_content: str
    answer: str



from pydantic import BaseModel, Field

class UserQueryCategory(BaseModel):
    category: Literal["qa", "summpdf", "quizpdf", "summtopic", "quiztopic"] = Field(
        ...,
        description=(
            "Category of the user query. Must be one of:\n"
            "- qa → Answer a question using retrieved pages from the PDF\n"
            "- summpdf → Summarize the entire PDF\n"
            "- quizpdf → Generate a 10-question quiz for the entire PDF\n"
            "- summtopic → Summarize a specific topic from the PDF\n"
            "- quiztopic → Generate a 10-question quiz on a specific topic from the PDF"
        )
    )
