package com.adi.agents.pdf.service;

import com.adi.agents.pdf.dao.PDFResponseDAO;
import com.adi.agents.pdf.entity.PDFResponseEntity;
import com.adi.agents.pdf.pojos.PDFResponse;
import com.adi.agents.pdf.dao.PDFResponseDAO;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
public class KafkaConsumerService {

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final PDFResponseDAO repository;

    public KafkaConsumerService(PDFResponseDAO repository) {
        this.repository = repository;
    }

    @KafkaListener(topics = "pdf-result", groupId = "pdf-result-group")
    public void consumeResult(String message) {
        try {
            PDFResponse response = objectMapper.readValue(message, PDFResponse.class);

            PDFResponseEntity entity = new PDFResponseEntity(
                    response.getWorkflowId(),
                    response.getData()
            );
            repository.save(entity);

            System.out.println("✅ Saved to H2: " + response.getWorkflowId());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
