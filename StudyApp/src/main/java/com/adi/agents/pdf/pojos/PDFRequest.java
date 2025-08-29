package com.adi.agents.pdf.pojos;

public class PDFRequest {
    private String userQuery;
    private String pdfPath;

    public PDFRequest(String userQuery, String pdfPath) {
        this.userQuery = userQuery;
        this.pdfPath = pdfPath;
    }

    public String getUserQuery() {
        return userQuery;
    }

    public void setUserQuery(String userQuery) {
        this.userQuery = userQuery;
    }

    public String getPdfPath() {
        return pdfPath;
    }

    public void setPdfPath(String pdfPath) {
        this.pdfPath = pdfPath;
    }
}
