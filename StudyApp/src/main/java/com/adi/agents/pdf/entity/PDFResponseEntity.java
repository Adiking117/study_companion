package com.adi.agents.pdf.entity;

import jakarta.persistence.*;

@Entity
public class PDFResponseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String workflowId;

    @Lob
    @Column(name = "data")
    private String data;

    public PDFResponseEntity() {}

    public PDFResponseEntity(String workflowId, String data) {
        this.workflowId = workflowId;
        this.data = data;
    }

    public Long getId() {
        return id;
    }

    public String getWorkflowId() {
        return workflowId;
    }

    public void setWorkflowId(String workflowId) {
        this.workflowId = workflowId;
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }
}
