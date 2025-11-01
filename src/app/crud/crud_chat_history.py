# src/app/crud/crud_chat_history.py

from sqlalchemy.orm import Session
from ..models.chat_history import ChatHistory
from ..schemas.chat_history import ChatHistoryCreateDB
from typing import List, Optional

# CREATE (새 채팅 기록 저장)
def create_chat_entry(
    db: Session, 
    chat_history_data: ChatHistoryCreateDB,
) -> ChatHistory:
    """새로운 질문/답변 기록을 DB에 저장합니다."""
    
    db_chat = ChatHistory(**chat_history_data.model_dump())
    
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    
    return db_chat

# READ (특정 PDF의 전체 채팅 기록 조회)
def get_chat_history_by_pdf_id(db: Session, pdf_id: int) -> List[ChatHistory]:
    """특정 PDF 파일 ID에 해당하는 모든 채팅 기록을 시간 순서로 조회합니다."""
    
    return db.query(ChatHistory).filter(ChatHistory.pdf_id == pdf_id).order_by(ChatHistory.timestamp).all()