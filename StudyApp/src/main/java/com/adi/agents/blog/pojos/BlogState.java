package com.adi.agents.blog.pojos;

import java.util.List;
import java.util.Map;

public class BlogState {
    private Map<String, String> input;   // ✅ input: { "text": "...", "image_url": "" }
    private String inputCategory;        // e.g. "link"
    private String youtubeVideoId;
    private String youtubeSubtitles;

    @Override
    public String toString() {
        return "BlogState{" +
                "input=" + input +
                ", inputCategory='" + inputCategory + '\'' +
                ", youtubeVideoId='" + youtubeVideoId + '\'' +
                ", youtubeSubtitles='" + youtubeSubtitles + '\'' +
                ", title='" + title + '\'' +
                ", content='" + content + '\'' +
                ", blog=" + blog +
                ", approved=" + approved +
                ", feedback='" + feedback + '\'' +
                ", feedback_history=" + feedback_history +
                ", postMedia='" + postMedia + '\'' +
                ", finalPost='" + finalPost + '\'' +
                ", image_url='" + image_url + '\'' +
                '}';
    }

    private String title;
    private String content;

    private Blog blog;                   // nested blog {title, content}
    private Boolean approved;
    private String feedback;
    private List<String> feedback_history;
    private String postMedia;
    private String finalPost;
    private String image_url;

    // --- Getters & Setters ---

    public Map<String, String> getInput() {
        return input;
    }

    public void setInput(Map<String, String> input) {
        this.input = input;
    }

    public String getInputCategory() {
        return inputCategory;
    }

    public void setInputCategory(String inputCategory) {
        this.inputCategory = inputCategory;
    }

    public String getYoutubeVideoId() {
        return youtubeVideoId;
    }

    public void setYoutubeVideoId(String youtubeVideoId) {
        this.youtubeVideoId = youtubeVideoId;
    }

    public String getYoutubeSubtitles() {
        return youtubeSubtitles;
    }

    public void setYoutubeSubtitles(String youtubeSubtitles) {
        this.youtubeSubtitles = youtubeSubtitles;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public Blog getBlog() {
        return blog;
    }

    public void setBlog(Blog blog) {
        this.blog = blog;
    }

    public Boolean getApproved() {
        return approved;
    }

    public void setApproved(Boolean approved) {
        this.approved = approved;
    }

    public String getFeedback() {
        return feedback;
    }

    public void setFeedback(String feedback) {
        this.feedback = feedback;
    }

    public String getPostMedia() {
        return postMedia;
    }

    public void setPostMedia(String postMedia) {
        this.postMedia = postMedia;
    }

    public String getImage_url() {
        return image_url;
    }

    public void setImage_url(String image_url) {
        this.image_url = image_url;
    }

    public String getFinalPost() {
        return finalPost;
    }

    public void setFinalPost(String finalPost) {
        this.finalPost = finalPost;
    }

    public List<String> getFeedback_history() {
        return feedback_history;
    }

    public void setFeedback_history(List<String> feedback_history) {
        this.feedback_history = feedback_history;
    }
}

