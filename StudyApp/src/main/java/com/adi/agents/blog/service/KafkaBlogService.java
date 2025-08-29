package com.adi.agents.blog.service;

import com.adi.agents.blog.dao.BlogDAO;
import com.adi.agents.blog.entity.BlogEntity;
import com.adi.agents.blog.pojos.BlogResponse;
import com.adi.agents.blog.pojos.FinalBlogResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class KafkaBlogService {

    private final KafkaTemplate<String, String> kafkaTemplate;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final BlogDAO blogRepository;

    public KafkaBlogService(KafkaTemplate<String, String> kafkaTemplate, BlogDAO blogRepository) {
        this.kafkaTemplate = kafkaTemplate;
        this.blogRepository = blogRepository;
    }

    // --- Producer Methods ---
    public void sendBlogOperation(String message) {
        kafkaTemplate.send("blog-operation", message);
    }

    public void sendBlogApproval(String message) {
        kafkaTemplate.send("blog-approval", message);
    }

    public void sendMediaChooser(String message) {
        kafkaTemplate.send("blog-mediachooser", message);
    }

    // --- Consumers ---
    @KafkaListener(topics = "blog-operation-result", groupId = "blog-op-result-group")
    public void consumeBlogOperationResult(String message) {
        try {
            BlogResponse response = objectMapper.readValue(message, BlogResponse.class);
            System.out.println("📩 Blog Operation Result: " + response);

            BlogEntity entity = new BlogEntity();
            entity.setWorkflowId(response.getWorkflowId());
            entity.setFinalBlog(null); // not ready yet

            // store state as JSON
            entity.setState(objectMapper.writeValueAsString(response.getState()));

            blogRepository.save(entity);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    /*
    *
    *
    * */

    @KafkaListener(topics = "blog-result", groupId = "blog-final-group")
    public void consumeBlogResult(String message) {
        try {
            FinalBlogResponse response = objectMapper.readValue(message, FinalBlogResponse.class);
            System.out.println("✅ Final Blog Received: " + response);

            blogRepository.findByWorkflowId(response.getWorkflowId()).ifPresentOrElse(
                    entity -> {
                        entity.setFinalBlog(response.getFinalBlog());
                        blogRepository.save(entity);
                    },
                    () -> {
                        BlogEntity entity = new BlogEntity();
                        entity.setWorkflowId(response.getWorkflowId());
                        entity.setFinalBlog(response.getFinalBlog());
                        blogRepository.save(entity);
                    }
            );

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
