# src/app/models/archiving_content.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from src.app.db.database import Base 

# 실제로 user가 보는 각 페이지 별 comment나 질문 답변 내용, user 마음대로 삭제가 가능해야함.
class ArchivingContent(Base):
    __tablename__ = "archiving_content"

    id = Column(Integer, primary_key=True, index=True)
    
    pdf_id = Column(Integer, ForeignKey("pdf_files.id"), nullable=False)
    
    page_number = Column(Integer, index=True, nullable=False)
    content = Column(Text, nullable=False)
    
    image_path = Column(String, nullable = True) 
    
    source_type = Column(String, nullable=False) # 'USER' 또는 'CHAT'
    
    last_modified = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False) 
    
    pdf_file = relationship("PdfFile", back_populates="archiving_contents")