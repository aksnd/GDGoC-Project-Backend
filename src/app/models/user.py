# src/app/models/pdf_file.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from src.app.db.database import Base 

class User(Base): 
    __tablename__ = "users"

    # 기본 키 (Primary Key)
    user_id = Column(String, primary_key=True)
    
    # 사용자 비밀번호 (생략 가능)
    password = Column(String, nullable=True)
    
    # 관계 정의 (다른 테이블에서 FK로 참조할 때 사용할 이름)
    pdf_files = relationship("PdfFile", back_populates="owner")