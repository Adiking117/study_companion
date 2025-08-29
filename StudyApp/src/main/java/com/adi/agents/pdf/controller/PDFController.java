package com.adi.agents.pdf.controller;

import com.adi.agents.pdf.dao.PDFResponseDAO;
import com.adi.agents.pdf.entity.PDFResponseEntity;
import com.adi.agents.pdf.pojos.PDFRequest;
import com.adi.agents.pdf.pojos.PDFResponse;
import com.adi.agents.pdf.service.KafkaProducerService;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/pdf")
public class PDFController {

    private final KafkaProducerService producerService;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final PDFResponseDAO repository;

    public PDFController(KafkaProducerService producerService, PDFResponseDAO repository) {
        this.producerService = producerService;
        this.repository = repository;
    }

    // --- Send event to Kafka ---
    @PostMapping("/query")
    public ResponseEntity<String> sendPdfRequest(@RequestBody PDFRequest pdfRequest) throws Exception {
        String workflowId = UUID.randomUUID().toString();

        ObjectNode messageNode = objectMapper.createObjectNode();
        messageNode.put("workflowId", workflowId);
        messageNode.put("userQuery", pdfRequest.getUserQuery());
        messageNode.put("pdfPath", pdfRequest.getPdfPath());

        String message = objectMapper.writeValueAsString(messageNode);
        producerService.sendMessage(message);

        return ResponseEntity.ok("📤 Event sent with workflowId: " + workflowId);
    }

    // --- Fetch result from H2 by workflowId ---
    @GetMapping("/query")
    public ResponseEntity<PDFResponseEntity> getResponse(@RequestParam String workflowId) {
        Optional<PDFResponseEntity> result = repository.findById(Long.valueOf(workflowId));
        return result.map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
