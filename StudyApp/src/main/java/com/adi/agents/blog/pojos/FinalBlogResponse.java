package com.adi.agents.blog.pojos;

public class FinalBlogResponse {
    private String workflowId;
    private String finalBlog;

    public String getWorkflowId() {
        return workflowId;
    }

    public void setWorkflowId(String workflowId) {
        this.workflowId = workflowId;
    }

    public String getFinalBlog() {
        return finalBlog;
    }

    public void setFinalBlog(String finalBlog) {
        this.finalBlog = finalBlog;
    }

    @Override
    public String toString() {
        return "FinalBlogResponse{" +
                "workflowId='" + workflowId + '\'' +
                ", finalBlog='" + finalBlog + '\'' +
                '}';
    }
}
