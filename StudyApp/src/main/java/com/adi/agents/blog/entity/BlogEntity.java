package com.adi.agents.blog.entity;

import com.adi.agents.blog.pojos.BlogState;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Data;

@Entity
@Data
public class BlogEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String workflowId;

    @Column(length = 5000)
    private String finalBlog;

    @Column(columnDefinition = "TEXT") // store as JSON
    private String state;  // <-- store serialized JSON
}

