import asyncio
import json
from aiokafka import AIOKafkaConsumer
from app.services.workflow import run_blog_workflow
from app.services import workflow_store
from sqlalchemy.orm import Session

KAFKA_BOOTSTRAP = "localhost:9092"
BLOG_APPROVAL_TOPIC = "blog-approval"


async def consume():
    db: Session = next(workflow_store.get_db())

    consumer = AIOKafkaConsumer(
        BLOG_APPROVAL_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="blog-approval-worker",
        auto_offset_reset="latest"
    )

    await consumer.start()
    print("✅ Blog Approval Worker started...")

    try:
        async for msg in consumer:
            try:
                data = json.loads(msg.value.decode("utf-8")) # type: ignore
                print(f"📩 Received blog approval request: {data}")

                workflow_id = data.get("workflowId")
                state = workflow_store.get_workflow(db, workflow_id)
                if not state:
                    print(f"⚠️ Workflow {workflow_id} not found")
                    continue

                state["approved"] = data.get("approved", False)
                state["feedback"] = data.get("feedback", "")

                state = run_blog_workflow(state, workflow_id)

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

                print(f"✅ Updated state after approval: {state}")

            except Exception as e:
                print(f"❌ Error: {e}")
    finally:
        await consumer.stop()
        db.close()


if __name__ == "__main__":
    asyncio.run(consume())
