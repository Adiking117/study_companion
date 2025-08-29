# Kafka-PDF-Workflow Project

This project demonstrates a **PDF query workflow** using **Spring Boot** and **Python** with **Kafka** for event-driven communication. The workflow involves sending PDF queries from Spring Boot to a Python consumer that processes the requests and sends results back to Spring Boot. H2 database is used for persistence.

---

## Architecture Overview

```
Spring Boot API --> Kafka(pdf-operation) --> Python Consumer
Python Consumer --> Kafka(pdf-result) --> Spring Boot Listener --> H2 DB
```

### Components

1. **Spring Boot Service**
   - Exposes REST endpoints for PDF queries.
   - Produces messages to Kafka (`pdf-operation`).
   - Consumes messages from Kafka (`pdf-result`) and saves results in H2 DB.

2. **Python Service**
   - Listens to Kafka topic `pdf-operation`.
   - Processes PDF query workflow (mock or real processing).
   - Sends results to Kafka topic `pdf-result`.

3. **Kafka**
   - Message broker for asynchronous communication.
   - Topics: `pdf-operation`, `pdf-result`.

4. **H2 Database**
   - Stores PDF workflow results.
   - On-disk persistence for durability.

5. **Docker**
   - Containerized Zookeeper and Kafka for local development.

---

## Prerequisites

- Java 17+
- Python 3.10+
- Docker
- Maven
- Kafka & Zookeeper Docker images

---

## Kafka & Zookeeper Setup (Docker)

```bash
# Start Zookeeper
docker run -d --name zookeeper -p 2181:2181 bitnami/zookeeper:latest

# Start Kafka
docker run -d --name kafka -p 9092:9092 \
    -e KAFKA_BROKER_ID=1 \
    -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
    -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
    -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 \
    bitnami/kafka:latest

# Create topics
docker exec -it kafka kafka-topics.sh --create --topic pdf-operation --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

docker exec -it kafka kafka-topics.sh --create --topic pdf-result --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

---

## Spring Boot Setup

### Dependencies (pom.xml)

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.kafka</groupId>
        <artifactId>spring-kafka</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
    </dependency>
</dependencies>
```

### application.properties

```properties
spring.application.name=agents
server.port=8080

# H2 persistent DB
spring.datasource.url=jdbc:h2:file:~/agentsdb;DB_CLOSE_ON_EXIT=FALSE;AUTO_SERVER=TRUE
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=password
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console

# Kafka
spring.kafka.bootstrap-servers=localhost:9092
spring.kafka.consumer.group-id=pdf-result-group
spring.kafka.consumer.auto-offset-reset=earliest
spring.kafka.consumer.key-deserializer=org.apache.kafka.common.serialization.StringDeserializer
spring.kafka.consumer.value-deserializer=org.apache.kafka.common.serialization.StringDeserializer
spring.kafka.producer.key-serializer=org.apache.kafka.common.serialization.StringSerializer
spring.kafka.producer.value-serializer=org.apache.kafka.common.serialization.StringSerializer
```

### Kafka Consumer Service

```java
@Service
@EnableKafka
public class KafkaConsumerService {
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final PDFResponseDAO repository;

    public KafkaConsumerService(PDFResponseDAO repository) {
        this.repository = repository;
    }

    @KafkaListener(topics = "pdf-result", groupId = "pdf-result-group")
    public void consumeResult(String message) {
        try {
            PDFResponseEntity response = objectMapper.readValue(message, PDFResponseEntity.class);
            repository.save(response);
            System.out.println("📩 Saved workflow result: " + response.getWorkflowId());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### Controller

```java
@RestController
@RequestMapping("/pdf")
public class PDFController {

    private final KafkaProducerService producerService;
    private final PDFResponseDAO repository;

    public PDFController(KafkaProducerService producerService, PDFResponseDAO repository) {
        this.producerService = producerService;
        this.repository = repository;
    }

    @PostMapping("/query")
    public ResponseEntity<String> sendPdfQuery(@RequestBody PDFRequest pdfRequest) throws Exception {
        String workflowId = UUID.randomUUID().toString();

        ObjectNode messageNode = new ObjectMapper().createObjectNode();
        messageNode.put("workflowId", workflowId);
        messageNode.put("userQuery", pdfRequest.getUserQuery());
        messageNode.put("pdfPath", pdfRequest.getPdfPath());

        producerService.sendMessage(messageNode.toString());
        return ResponseEntity.ok("📤 Event sent with workflowId: " + workflowId);
    }

    @GetMapping("/query")
    public Optional<PDFResponseEntity> getResponse(@RequestParam String workflowId) {
        return repository.findById(workflowId);
    }
}
```

---

## Python Consumer (FastAPI optional)

```python
import asyncio
import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

KAFKA_BOOTSTRAP = "localhost:9092"
PDF_OPERATION_TOPIC = "pdf-operation"
PDF_RESULT_TOPIC = "pdf-result"
CONSUMER_GROUP = None

async def consume():
    consumer = AIOKafkaConsumer(PDF_OPERATION_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP, group_id=CONSUMER_GROUP, auto_offset_reset="latest")
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)

    await consumer.start()
    await producer.start()
    print("✅ Python consumer started...")

    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode('utf-8'))
            workflow_id = data.get("workflowId")
            response = {"workflowId": workflow_id, "data": "Hello"}
            await producer.send_and_wait(PDF_RESULT_TOPIC, json.dumps(response).encode('utf-8'))
            print(f"📤 Sent result: {response}")
    finally:
        await consumer.stop()
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(consume())
```

---

## Notes

- Kafka consumer groups: Python consumer can run without a group id to avoid `GroupCoordinatorNotAvailableError`. Spring Boot must have a **stable group id**.
- H2 database persists locally using `jdbc:h2:file:~/agentsdb`. Check at `~/agentsdb.mv.db`.
- Use Postman to send PDF queries and retrieve results via GET endpoint.
- Docker simplifies running Kafka + Zookeeper locally without installing them natively.

---

## References

- [Spring Kafka Documentation](https://docs.spring.io/spring-kafka/reference/html/)
- [AIoKafka Documentation](https://aiokafka.readthedocs.io/en/stable/)
- [H2 Database](https://www.h2database.com/html/main.html)

