# src/app/api/chat.py

from fastapi import APIRouter, Depends, status, File, UploadFile, Form, HTTPException 
from sqlalchemy.orm import Session
from ..db.database import get_db

# 💡 TODO: schemas, services 모듈은 추후 완성됩니다.

router = APIRouter(
    prefix="/chat",
    tags=["Gemini Chat & History"]
)

# 예시: POST /chat/query - Gemini 질의 및 기록 저장
@router.post("/query")
def process_chat_query(
    image_file: UploadFile = File(..., description="드래그한 이미지 파일"),
    
    public_id: str = Form(..., description= "pdf의 공개 id"),
    page_number: int = Form(..., description= "질문이 발생한 PDF 페이지 번호"),
    question_query: str = Form(..., description= "질문 query"),
    
    db: Session = Depends(get_db),
):
    """
    [API Layer] 사용자 질문, 페이지 정보를 받아 Gemini에게 질의하고 기록을 저장합니다.
    """
    # answer = get_gemini_response_and_save(db, query_data) # services 호출 (추후 구현)
    return {"message": "Query processed, response received and saved."}