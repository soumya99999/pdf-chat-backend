from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.services import nlp_processor

router = APIRouter()

@router.post("/ask", response_model=schemas.AnswerResponse)
def ask_question(
    request: schemas.QuestionRequest,
    db: Session = Depends(get_db)
):
    db_doc = crud.get_document_by_id(db, request.document_id)
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if not db_doc.content:
        raise HTTPException(status_code=400, detail="Document content is empty")

    try:
        answer = nlp_processor.answer_question(db_doc.content, request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return schemas.AnswerResponse(answer=answer)
