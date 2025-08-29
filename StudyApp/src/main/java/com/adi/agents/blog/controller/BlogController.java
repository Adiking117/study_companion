package com.adi.agents.blog.controller;

import com.adi.agents.blog.dao.BlogDAO;
import com.adi.agents.blog.entity.BlogEntity;
import com.adi.agents.blog.pojos.*;
import com.adi.agents.blog.service.KafkaBlogService;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/blog")
public class BlogController {

    private final KafkaBlogService blogService;
    private final BlogDAO repository;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public BlogController(KafkaBlogService blogService, BlogDAO repository) {
        this.blogService = blogService;
        this.repository = repository;
    }

    @PostMapping("/start")
    public ResponseEntity<String> startBlog(@RequestBody BlogRequest req) throws Exception {
        String workflowId = UUID.randomUUID().toString();

        ObjectNode message = objectMapper.createObjectNode();
        message.put("workflowId", workflowId);
        message.put("text", req.getText());
        message.put("image_url", req.getImageUrl());

        blogService.sendBlogOperation(message.toString());
        return ResponseEntity.ok("📤 Blog Operation started. WorkflowId: " + workflowId);
    }

    @PostMapping("/approve")
    public ResponseEntity<String> approveBlog(@RequestBody BlogApprovalRequest req) throws Exception {
        String message = objectMapper.writeValueAsString(req);
        blogService.sendBlogApproval(message);
        return ResponseEntity.ok("📤 Approval sent for WorkflowId: " + req.getWorkflowId());
    }

    @PostMapping("/choosemedia")
    public ResponseEntity<String> chooseMedia(@RequestBody BlogMediaRequest req) throws Exception {
        String message = objectMapper.writeValueAsString(req);
        blogService.sendMediaChooser(message);
        return ResponseEntity.ok("📤 Media choice sent for WorkflowId: " + req.getWorkflowId());
    }

    @GetMapping("/{workflowId}")
    public ResponseEntity<Optional<BlogEntity>> getBlog(@PathVariable String workflowId) {
        return ResponseEntity.ok(repository.findByWorkflowId(workflowId));
    }
}
