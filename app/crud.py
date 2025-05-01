from sqlalchemy.orm import Session
from app import models, schemas

def create_document(db: Session, filename: str, content: str):
    db_doc = models.Document(filename=filename, content=content)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def get_document_by_id(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def get_document_by_filename(db: Session, filename: str):
    return db.query(models.Document).filter(models.Document.filename == filename).first()
