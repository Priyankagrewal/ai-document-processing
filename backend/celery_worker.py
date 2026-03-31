from celery import Celery
import time
import redis
from sqlalchemy.orm import Session
import database, models

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

r = redis.Redis(host='localhost', port=6379, db=0)

@celery.task(bind=True)
def process_document(self, file_path, doc_id):

    db = database.SessionLocal()

    try:
        # Update status → processing
        doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
        if doc:
            doc.status = "processing"
            db.commit()

        r.set("latest_progress", "job_started")
        time.sleep(5)

        r.set("latest_progress", "parsing_started")
        time.sleep(5)

        r.set("latest_progress", "parsing_completed")

        r.set("latest_progress", "extraction_started")
        time.sleep(5)

        r.set("latest_progress", "extraction_completed")

        # Final update
        if doc:
            doc.status = "completed"
            doc.result = "Processed successfully"
            db.commit()

        r.set("latest_progress", "job_completed")

        return {"status": "completed"}

    except Exception as e:
        if doc:
            doc.status = "failed"
            db.commit()

        r.set("latest_progress", "job_failed")
        return {"status": "failed"}

    finally:
        db.close()