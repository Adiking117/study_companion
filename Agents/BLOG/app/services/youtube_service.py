import re
from youtube_transcript_api import YouTubeTranscriptApi
from app.models.state import BlogState

YOUTUBE_REGEX = r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|v/))([a-zA-Z0-9_-]{11})"

def determine_input(state: BlogState):
    """
    Determine whether input is YouTube link or custom topic.
    """
    input_data = state.get("input", {})
    if not isinstance(input_data, dict):
        raise ValueError("State 'input' must be a dict with keys 'text' and optional 'image_url'")

    input_text = input_data.get("text", "").strip()
    image_url = input_data.get("image_url", "").strip()

    match = re.search(YOUTUBE_REGEX, input_text)
    if match:
        return {
            "inputCategory": "link",
            "youtubeVideoId": match.group(1),
            "image_url": image_url
        }
    else:
        return {
            "inputCategory": "topic",
            "topic": input_text,
            "image_url": image_url
        }

def fetch_youtube_subtitles(state: BlogState):
    """
    Fetch subtitles for a YouTube video.
    """
    video_id = state.get("youtubeVideoId")
    if not video_id:
        raise ValueError("youtubeVideoId not found in state")

    try:
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        combined_text = " ".join(snippet.text for snippet in fetched_transcript)
        return {"youtubeSubtitles": combined_text}
    except Exception as e:
        raise RuntimeError(f"Failed to fetch subtitles for video {video_id}: {str(e)}")
