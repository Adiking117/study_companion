import asyncio
import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app.services.workflow import run_blog_workflow
from app.services import workflow_store
from app.models.state import BlogState
from sqlalchemy.orm import Session

KAFKA_BOOTSTRAP = "localhost:9092"
BLOG_OPERATION_TOPIC = "blog-operation"
BLOG_OPERATION_RESULT_TOPIC = "blog-operation-result"


async def consume():
    db: Session = next(workflow_store.get_db())

    consumer = AIOKafkaConsumer(
        BLOG_OPERATION_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="blog-operation-worker",
        auto_offset_reset="latest"
    )
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)

    await consumer.start()
    await producer.start()
    print("✅ Blog Operation Worker started...")

    try:
        async for msg in consumer:
            try:
                data = json.loads(msg.value.decode("utf-8")) # type: ignore
                print(f"📩 Received blog operation request: {data}")

                workflow_id = data.get("workflowId")
                initial_state: BlogState = {
                    "input": {
                        "text": data.get("text", ""),
                        "image_url": data.get("image_url", "")
                    }
                }

                workflow_id = workflow_store.create_workflow(db,initial_state,workflow_id)

                # Run workflow until pause
                state = run_blog_workflow(initial_state, workflow_id)

                # state = {
                #         "input": {
                #             "text": "https://www.youtube.com/watch?v=Tap6SEf0Er4&list=LL&index=110&ab_channel=Smoah",
                #             "image_url": "",
                #         },
                #         "inputCategory": "link",
                #         "youtubeVideoId": "Tap6SEf0Er4",
                #         "youtubeSubtitles": "sometext",
                #         "title": "sometext",
                #         "content": "sometext",
                #         "blog": {
                #             "title": "sometext",
                #             "content": "sometext",
                #         },
                #         "approved": None,
                #         "feedback_history": [],
                #         "image_url": "",
                #     }
                workflow_store.update_workflow(db, workflow_id, state)

                response = {
                    "workflowId": workflow_id,
                    "status": "paused",
                    "pauseReason": "waiting_for_approval",
                    "state": state
                }

                await producer.send_and_wait(
                    BLOG_OPERATION_RESULT_TOPIC,
                    json.dumps(response).encode("utf-8")
                )
                print(f"📤 Sent blog operation result: {response}")

            except Exception as e:
                print(f"❌ Error: {e}")
    finally:
        await consumer.stop()
        await producer.stop()
        db.close()


if __name__ == "__main__":
    asyncio.run(consume())
