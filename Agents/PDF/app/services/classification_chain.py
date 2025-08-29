from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from app.dependencies import get_chat_model
from app.models.state import UserQueryCategory

def get_classification_chain():
        
    # Parser
    parser = PydanticOutputParser(pydantic_object=UserQueryCategory)

    # Prompt template with stricter instruction
    classification_prompt = ChatPromptTemplate.from_messages([
        ("system",
        "You are a query classifier. "
        "Classify the user query into exactly one of these categories: "
        "qa, summpdf, quizpdf, summtopic, quiztopic. "
        "Return ONLY a valid JSON object, with no extra text."),
        ("human", "Query: {query}\n\n{format_instructions}")
    ]).partial(format_instructions=parser.get_format_instructions())

    # Classification chain
    classification_chain = classification_prompt | get_chat_model() | parser

    return classification_chain
