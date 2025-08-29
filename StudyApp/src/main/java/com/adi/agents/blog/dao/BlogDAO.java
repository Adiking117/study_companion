package com.adi.agents.blog.dao;

import com.adi.agents.blog.entity.BlogEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface BlogDAO extends JpaRepository<BlogEntity, Long> {
    Optional<BlogEntity> findByWorkflowId(String workflowId);
}
