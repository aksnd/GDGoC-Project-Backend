# src/app/models/pdf_file.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

# Base는 src/app/db/database.py 에서 정의되어 있다고 가정합니다.
from src.app.db.database import Base 

def generate_public_uuid():
    """UUID4를 문자열로 변환하여 public_id를 생성합니다."""
    return str(uuid.uuid4())

class PdfFile(Base): # ⭐ 클래스 이름 변경: PdfFile
    __tablename__ = "pdf_files" # ⭐ 테이블 이름 변경: pdf_files

    id = Column(Integer, primary_key=True, index=True)
    
    # Front에서 사용되는 고유 ID. UUID로 자동 생성하며 Unique 제약조건 부여.
    public_id = Column(String, unique=True, index=True, default=generate_public_uuid, nullable=False) 
    
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False) # GCP Storage 경로 등
    
    upload_time = Column(DateTime, default=datetime.now(timezone.utc), nullable=False) 
    
    # 관계 정의 (다른 테이블에서 FK로 참조할 때 사용할 이름)
    chat_histories = relationship("ChatHistory", back_populates="pdf_project") 
    archiving_contents = relationship("ArchivingContent", back_populates="pdf_project")