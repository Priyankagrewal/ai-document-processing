from sqlalchemy.orm import Session
import models

def create_document(db: Session, filename: str):
    doc = models.Document(filename=filename, status="queued")
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def get_documents(db: Session):
    return db.query(models.Document).all()

def get_document_by_id(db: Session, doc_id: int):
    return db.query(models.Document).filter(models.Document.id == doc_id).first()

def update_document(db: Session, doc_id: int, result: str):
    doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if doc:
        doc.result = result
        db.commit()
        db.refresh(doc)
    return doc