package com.adi.agents.pdf.pojos;

public class PDFResponse {
    private String workflowId;
    private String data;

    public PDFResponse() {
        // default constructor required for Jackson
    }

    public PDFResponse(String data, String workflowId) {
        this.data = data;
        this.workflowId = workflowId;
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }

    public String getWorkflowId() {
        return workflowId;
    }

    public void setWorkflowId(String workflowId) {
        this.workflowId = workflowId;
    }
}
