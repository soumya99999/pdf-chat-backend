import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app import crud, schemas, config
from app.database import get_db
from app.services import pdf_processor

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload", response_model=schemas.DocumentResponse)
async def upload_pdf(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    logger.info(f"Received upload request headers: {request.headers}")
    logger.info(f"Received upload request for file: {file.filename}")

    if not file.filename.lower().endswith(".pdf"):
        logger.warning(f"Rejected upload due to unsupported file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_location = os.path.join(config.UPLOAD_DIR, file.filename)
    logger.info(f"File will be saved to: {file_location}")

    if os.path.exists(file_location):
        logger.warning(f"Rejected upload because file already exists: {file_location}")
        raise HTTPException(status_code=400, detail="File with this name already exists")

    try:
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        logger.info(f"File saved successfully: {file_location}")
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    try:
        text = pdf_processor.extract_text_from_pdf(file_location)
        logger.info(f"Extracted text from PDF: {file.filename}")
    except Exception as e:
        os.remove(file_location)
        logger.error(f"Failed to extract text from PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    try:
        db_doc = crud.create_document(db, filename=file.filename, content=text)
        logger.info(f"Saved document metadata to database: {file.filename}")
    except Exception as e:
        os.remove(file_location)
        logger.error(f"Failed to save document metadata: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save document metadata: {e}")

    return db_doc
