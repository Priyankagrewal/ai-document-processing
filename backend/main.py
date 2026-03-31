from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.orm import Session
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware

import models, database, crud

# ✅ Celery safe import
try:
    from celery_worker import process_document
    CELERY_AVAILABLE = True
except:
    CELERY_AVAILABLE = False

# ✅ Redis safe import
try:
    import redis
    r = redis.Redis(host='localhost', port=6379, db=0)
except:
    r = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

@app.post("/upload")
async def upload(file: UploadFile, db: Session = Depends(get_db)):
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = crud.create_document(db, file.filename)

    if CELERY_AVAILABLE:
        try:
            process_document.delay(file_path, doc.id)
        except:
            print("Celery failed")
    else:
        print("Fallback mode")

    return {"message": "File uploaded", "doc_id": doc.id}

@app.get("/documents")
def get_all_documents(db: Session = Depends(get_db)):
    docs = crud.get_documents(db)
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "status": d.status,
            "result": d.result
        }
        for d in docs
    ]

@app.post("/retry/{doc_id}")
def retry_document(doc_id: int, db: Session = Depends(get_db)):
    doc = crud.get_document_by_id(db, doc_id)

    file_path = f"uploads/{doc.filename}"
    doc.status = "queued"
    db.commit()

    if CELERY_AVAILABLE:
        try:
            process_document.delay(file_path, doc.id)
        except:
            print("Retry failed")

    return {"message": "Retry started"}

@app.put("/documents/{doc_id}")
def update_document(doc_id: int, result: str, db: Session = Depends(get_db)):
    crud.update_document(db, doc_id, result)
    return {"message": "Updated"}

@app.get("/progress")
def get_progress():
    if r:
        progress = r.get("latest_progress")
        if progress:
            return {"progress": progress.decode()}
    return {"progress": "fallback_mode"}
