import os
import requests
from app.models.state import BlogState
from app.config import settings

def publish_blog_to_facebook(final_blog: dict) -> dict:
    """
    Publish a blog to Facebook Page feed.
    """
    page_id = settings.FACEBOOK_PAGE_ID
    page_access_token = settings.FACEBOOK_PAGE_TOKEN
    graph_api_version = settings.FACEBOOK_GRAPH_API_VERSION

    if not page_id or not page_access_token:
        raise RuntimeError("Missing FACEBOOK_PAGE_ID or FACEBOOK_PAGE_TOKEN")

    message_text = f"{final_blog.get('title', '')}\n\n{final_blog.get('content', '')}"

    post_url = f"https://graph.facebook.com/{graph_api_version}/{page_id}/feed"
    post_params = {"message": message_text, "access_token": page_access_token}

    post_resp = requests.post(post_url, data=post_params)
    if not post_resp.ok:
        raise RuntimeError(f"Failed to publish post: {post_resp.text}")
    post_id = post_resp.json().get("id")

    get_url = f"https://graph.facebook.com/{graph_api_version}/{post_id}"
    get_params = {"fields": "id,message,created_time", "access_token": page_access_token}
    get_resp = requests.get(get_url, params=get_params)
    if not get_resp.ok:
        raise RuntimeError(f"Failed to retrieve post data: {get_resp.text}")

    return get_resp.json()

def publish_blog_to_instagram(final_blog: dict,image_url: str) -> dict:
    """
    Publish a blog post to Instagram.
    """
    ig_account_id = settings.INSTAGRAM_PAGE_ID
    access_token = settings.FACEBOOK_PAGE_TOKEN
    graph_api_version = settings.FACEBOOK_GRAPH_API_VERSION

    blog = final_blog

    if not blog:
        raise ValueError("No blog found in state to publish")
    if not image_url:
        raise ValueError("No image_url found for Instagram post")

    caption_text = f"{blog.get('title', '')}\n\n{blog.get('content', '')}"

    media_url = f"https://graph.facebook.com/{graph_api_version}/{ig_account_id}/media"
    media_params = {"image_url": image_url, "caption": caption_text, "access_token": access_token}
    media_resp = requests.post(media_url, data=media_params)
    if not media_resp.ok:
        raise RuntimeError(f"Failed to create Instagram media: {media_resp.text}")
    media_id = media_resp.json().get("id")

    publish_url = f"https://graph.facebook.com/{graph_api_version}/{ig_account_id}/media_publish"
    publish_params = {"creation_id": media_id, "access_token": access_token}
    publish_resp = requests.post(publish_url, data=publish_params)
    if not publish_resp.ok:
        raise RuntimeError(f"Failed to publish Instagram post: {publish_resp.text}")

    return publish_resp.json()



from typing import Dict

def publish_to_facebook_node(state: BlogState) -> Dict:
    """
    LangGraph node wrapper for publishing a blog post to Facebook.
    Uses the `publish_blog_to_facebook` function.
    Updates state with 'finalpost'.
    """
    blog = state.get("blog", {})
    if not blog:
        raise ValueError("No blog found in state to publish")

    try:
        result = publish_blog_to_facebook(blog)
        return {"finalpost": result}
    except Exception as e:
        raise RuntimeError(f"Facebook publishing failed: {str(e)}")



def publish_to_instagram_node(state: BlogState) -> Dict:
    """
    LangGraph node wrapper for Instagram publishing.
    Uses state's image_url.
    Updates state with 'finalpost'.
    """
    blog = state.get("blog", {})
    image_url = state.get("image_url")

    if not blog:
        raise ValueError("No blog found in state to publish")
    if not image_url:
        raise ValueError("No image_url found in state for Instagram post")

    try:
        result = publish_blog_to_instagram(blog, image_url)
        return {"finalpost": result}
    except Exception as e:
        raise RuntimeError(f"Instagram publishing failed: {str(e)}")
