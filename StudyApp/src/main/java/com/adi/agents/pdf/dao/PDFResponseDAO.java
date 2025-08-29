package com.adi.agents.pdf.dao;

import com.adi.agents.pdf.entity.PDFResponseEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PDFResponseDAO extends JpaRepository<PDFResponseEntity, Long> {
}

