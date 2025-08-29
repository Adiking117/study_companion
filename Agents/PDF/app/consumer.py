import asyncio
import json
import signal
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app.services import workflow_store
from app.models.state import PDFChatState
from sqlalchemy.orm import Session
from app.services.workflow import run_blog_workflow

# Kafka settings
KAFKA_BOOTSTRAP = "localhost:9092"
PDF_OPERATION_TOPIC = "pdf-operation"
PDF_RESULT_TOPIC = "pdf-result"
# CONSUMER_GROUP = "pdf-operation-worker"   # stable group id
CONSUMER_GROUP = None   # stable group id


class PDFWorker:
    def __init__(self):
        self.consumer = None
        self.producer = None
        self.db: Session = None # type: ignore
        self.should_stop = asyncio.Event()

    async def start(self):
        # DB session (manual, no FastAPI Depends here)
        self.db = next(workflow_store.get_db())

        # Kafka consumer
        self.consumer = AIOKafkaConsumer(
            PDF_OPERATION_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP,
            group_id=CONSUMER_GROUP,
            auto_offset_reset="latest"
        )

        # Kafka producer
        self.producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)

        # Start connections
        await self.consumer.start()
        await self.producer.start()
        print("✅ Python consumer started, listening for PDF operations...")

    async def process_messages(self):
        try:
            async for msg in self.consumer: # type: ignore
                try:
                    data = json.loads(msg.value.decode("utf-8"))  # type: ignore
                    print(f"📩 Received request: {data}")

                    workflow_id = data.get("workflowId")
                    if not workflow_id:
                        print("⚠️ Missing workflowId in request, skipping...")
                        continue

                    # Build initial workflow state
                    initial_state: PDFChatState = {
                        "userQuery": data.get("userQuery", ""),
                        "pdfpath": data.get("pdfPath", "")
                    }

                    # --- Workflow DB logic could go here ---
                    workflow_store.create_workflow(self.db, initial_state, workflow_id=workflow_id)
                    state = run_blog_workflow(initial_state, workflow_id)
                    workflow_store.update_workflow(self.db, workflow_id, state)

                    response = {
                        "workflowId": workflow_id,
                        "data": state.get("answer")
                    }

                    await self.producer.send_and_wait( # type: ignore
                        PDF_RESULT_TOPIC,
                        json.dumps(response).encode("utf-8")
                    )
                    print(f"📤 Sent result: {response}")

                except Exception as e:
                    print(f"❌ Error processing message: {e}")

                if self.should_stop.is_set():
                    break

        finally:
            await self.stop()

    async def stop(self):
        print("⛔ Shutting down consumer/producer...")
        if self.consumer:
            await self.consumer.stop()
        if self.producer:
            await self.producer.stop()
        if self.db:
            self.db.close()
        print("✅ Shutdown complete.")


async def main():
    worker = PDFWorker()

    await worker.start()

    try:
        await worker.process_messages()
    except KeyboardInterrupt:
        print("🛑 KeyboardInterrupt received, stopping...")
        await worker.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Application interrupted by user.")
