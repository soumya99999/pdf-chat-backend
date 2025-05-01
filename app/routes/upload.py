import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app import crud, schemas, config
from app.database import get_db
from app.services import pdf_processor, cloudinary_service

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

    try:
        content = await file.read()
    except Exception as e:
        logger.error(f"Failed to read file content: {e}")
        raise HTTPException(status_code=500, detail="Failed to read file content")

    try:
        text = pdf_processor.extract_text_from_pdf_bytes(content)
        logger.info(f"Extracted text from PDF: {file.filename}")
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to extract text from PDF: {str(e)}")

    try:
        cloudinary_url = cloudinary_service.upload_pdf_to_cloudinary(content, file.filename)
        logger.info(f"Uploaded PDF to Cloudinary: {cloudinary_url}")
    except RuntimeError as e:
        logger.error(f"Cloudinary upload failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during Cloudinary upload: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload PDF to Cloudinary")

    try:
        db_doc = crud.create_document(db, filename=file.filename, content=text, cloudinary_url=cloudinary_url)
        logger.info(f"Saved document metadata to database: {file.filename}")
    except Exception as e:
        logger.error(f"Failed to save document metadata: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save document metadata: {str(e)}")

    return db_doc
