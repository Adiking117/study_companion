from app.dependencies import get_chat_model
from app.models.state import BlogState

chat_model = get_chat_model()



def parallel_title_content_start(state: BlogState):
    print("Starting generation with existing:", state.get("title"), state.get("content"))


def generate_blog_title(state: BlogState):
    transcript = state.get("youtubeSubtitles")
    if not transcript:
        raise ValueError("Transcript not found in state")

    feedback = state.get("feedback", "")
    feedback_history = state.get("feedback_history", [])

    prompt = f"""You are a professional blog writer.
Generate exactly ONE engaging, SEO-friendly blog title.
Rules:
- Only output the title (no explanations, no options).
- Keep it concise, catchy, and interesting.
- Do not include phrases like "Here are some options".
- Avoid quotation marks around the title.

Transcript:
{transcript}

Feedback: {feedback}
Previous Feedback: {feedback_history}
"""
    response = chat_model.invoke(prompt)
    return {"title": getattr(response, "content", str(response)).strip()}




def generate_blog_content(state: BlogState):
    transcript = state.get("youtubeSubtitles")
    if not transcript:
        raise ValueError("Transcript not found in state")

    feedback = state.get("feedback", "")
    feedback_history = state.get("feedback_history", [])

    prompt = f"""You are a professional content creator.
Expand the following transcript into a structured, reader-friendly blog post.
Rules:
- Write in clear paragraphs with headings.
- Include an Introduction, Body (with sections), and Conclusion.
- Keep the writing engaging but concise.
- Only output the blog text (no explanations, no meta comments).
- Do not include phrases like "Here's the blog".

Transcript:
{transcript}

Feedback: {feedback}
Previous Feedback: {feedback_history}
"""
    response = chat_model.invoke(prompt)
    return {"content": getattr(response, "content", str(response)).strip()}



def compose_final_blog(state: BlogState):
    title = state.get("title")
    content = state.get("content")
    if not title or not content:
        raise ValueError("Both title and content must be present")

    # feedback = state.get("feedback", "")
    # feedback_history = state.get("feedback_history", [])

    # prompt = f"""Refine the following draft blog into a polished post.

    # Title:
    # {title}

    # Content:
    # {content}

    # Feedback: {feedback}
    # Previous Feedback: {feedback_history}
    # """
    # response = chat_model.invoke(prompt)
    # return {
    #     "blog": {
    #         "title": title.strip(),
    #         "content": getattr(response, "content", str(response)).strip()
    #     }
    # }
    return {
        "blog": {
            "title": title.strip(),
            "content": content
        }
    }
