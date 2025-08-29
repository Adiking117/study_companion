package com.adi.agents.blog.pojos;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class BlogApprovalRequest {
    private String workflowId;
    private boolean approved;
    private String feedback;
}
