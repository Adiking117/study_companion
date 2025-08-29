from typing import Dict
from app.models.state import BlogState
import traceback

def human_approval_node(state: BlogState) -> Dict:  # type: ignore
    try:
        blog = state.get("blog", {})
        if not blog:
            raise ValueError("No blog found in state to review")

        approved = state.get("approved")
        feedback_history = state.get("feedback_history", [])

        # Case 1: No approval yet → pause workflow
        if approved is None:
            print("[DEBUG] Pausing for approval:")
            return {"approved": None, "blog": blog, "feedback_history": feedback_history}

        # Case 2: Blog rejected → add feedback and pause again
        if approved is False:
            feedback = state.get("feedback", "")
            # if feedback:
            #     feedback_history.append(feedback)  # track all feedbacks
            print("[DEBUG] Blog rejected, waiting for regeneration")
            return {
                "approved": None,  # reset so workflow pauses again
                "blog": blog,
                "feedback_history": feedback_history,
            }

        # Case 3: Blog approved → continue workflow
        if approved is True:
            print("[DEBUG] Blog approved")
            return {"approved": True, "blog": blog, "feedback_history": feedback_history}

    except Exception as e:
        print("[ERROR] human_approval_node crashed")
        traceback.print_exc()
        raise


def choose_post_media_node(state: BlogState) -> Dict:
    """
    HITL node for choosing post media.
    Expects `postMedia` field in state: "fb" or "instagram".
    Pauses workflow until a valid choice is set.
    """
    post_media = state.get("postMedia")
    if not post_media:
        raise RuntimeError("PAUSE: waiting for human to choose media")
    
    blog = state.get("blog", {})
    if not blog:
        raise ValueError("No blog found in state")

    if post_media not in ["fb", "instagram"]:
        # Pause workflow
        return {"postMedia": None}

    return {"postMedia": post_media}
