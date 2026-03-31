import os
from celery import Celery
import time

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery.task
def process_document(file_path, doc_id):
    print(f"Processing {file_path}")
    time.sleep(5)
    return {"status": "completed"}
