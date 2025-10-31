# src/app/models/archiving_content.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from src.app.db.database import Base 

class ArchivingContent(Base):
    __tablename__ = "archiving_content"

    id = Column(Integer, primary_key=True, index=True)
    
    project_id = Column(Integer, ForeignKey("pdf_files.id"), nullable=False)
    
    page_number = Column(Integer, index=True, nullable=False)
    content = Column(Text, nullable=False)
    
    source_type = Column(String, nullable=False) # 'USER' 또는 'CHAT'
    
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) 
    
    project_pdf = relationship("PdfFile", back_populates="archiving_contents")