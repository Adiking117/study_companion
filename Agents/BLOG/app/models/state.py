from typing import TypedDict, Literal, Dict, List
import operator
from typing_extensions import Annotated

class BlogState(TypedDict, total=False):
    # User input
    input: dict
    inputCategory: Literal["link", "topic"]

    # YouTube details
    youtubeVideoId: str
    topic: str
    youtubeSubtitles: str

    # Generated content
    title: str
    content: str
    blog: Dict

    # Human-in-the-loop approval
    approved: bool
    feedback: str
    feedback_history: Annotated[List[str], operator.add]
    retries: int
    max_retries: int


    # Posting destination
    postMedia: Literal["fb", "instagram"]

    # Instagram-only
    image_url: str

    # Final post structure
    finalpost: Dict
