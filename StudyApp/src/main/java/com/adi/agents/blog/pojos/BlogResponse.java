package com.adi.agents.blog.pojos;

import java.util.Map;

public class BlogResponse {
    private String workflowId;
    private String status;
    private String pauseReason;
    private BlogState state; // <-- Strongly typed

    public BlogResponse() {
    }

    public String getWorkflowId() {
        return workflowId;
    }

    public void setWorkflowId(String workflowId) {
        this.workflowId = workflowId;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getPauseReason() {
        return pauseReason;
    }

    public void setPauseReason(String pauseReason) {
        this.pauseReason = pauseReason;
    }

    public BlogState getState() {
        return state;
    }

    @Override
    public String toString() {
        return "BlogResponse{" +
                "workflowId='" + workflowId + '\'' +
                ", status='" + status + '\'' +
                ", pauseReason='" + pauseReason + '\'' +
                ", state=" + state +
                '}';
    }

    public void setState(BlogState state) {
        this.state = state;
    }
}



