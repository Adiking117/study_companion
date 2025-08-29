package com.adi.agents.blog.pojos;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class BlogMediaRequest {
    private String workflowId;
    private String postMedia; // fb or instagram
}
