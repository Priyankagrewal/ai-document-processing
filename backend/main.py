from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.orm import Session
import shutil
import os
import webbrowser
import redis
import csv
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import models, database, crud
from celery_worker import process_document

app = FastAPI()

# ✅ CORS (IMPORTANT FOR FRONTEND CONNECTION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def open_browser():
    webbrowser.open("http://127.0.0.1:8000/docs")

models.Base.metadata.create_all(bind=database.engine)

r = redis.Redis(host='localhost', port=6379, db=0)

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

    r.set("latest_progress", "queued")

    process_document.delay(file_path, doc.id)

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

    process_document.delay(file_path, doc.id)

    return {"message": "Retry started"}

@app.put("/documents/{doc_id}")
def update_document(doc_id: int, result: str, db: Session = Depends(get_db)):
    doc = crud.update_document(db, doc_id, result)
    return {"message": "Updated"}

@app.get("/progress")
def get_progress():
    progress = r.get("latest_progress")
    if progress:
        return {"progress": progress.decode()}
    return {"progress": "waiting"}

@app.get("/export/json")
def export_json(db: Session = Depends(get_db)):
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

@app.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    docs = crud.get_documents(db)
    file_path = "export.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "filename", "status", "result"])

        for d in docs:
            writer.writerow([d.id, d.filename, d.status, d.result])

    return FileResponse(file_path, media_type='text/csv', filename="documents.csv")