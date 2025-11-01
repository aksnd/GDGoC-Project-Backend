# src/app/models/chat_history.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from src.app.db.database import Base 

# 단순한 chat_history 역할로, USER가 PDF 기반으로 보는 용도의 DB는 아님 (User 삭제 불가)
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    
    pdf_id = Column(Integer, ForeignKey("pdf_files.id"), nullable=False) 
    
    page_number = Column(Integer, nullable=False)
    question_query = Column(Text, nullable=False)
    response_query = Column(Text, nullable=False)
    
    image_path = Column(String) 
    
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    pdf_file = relationship("PdfFile", back_populates="chat_histories")