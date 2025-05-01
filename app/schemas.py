from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentCreate(BaseModel):
    filename: str

class DocumentResponse(BaseModel):
    id: int
    filename: str
    upload_date: datetime

    class Config:
        from_attributes = True  # updated for Pydantic v2

class QuestionRequest(BaseModel):
    document_id: int
    question: str

class AnswerResponse(BaseModel):
    answer: str
