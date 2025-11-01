# src/app/crud/crud_pdf_file.py

from sqlalchemy.orm import Session
from ..models.pdf_file import PdfFile
from ..schemas.pdf import PdfContentCreateDB 
from typing import Optional

# CREATE (새 PDF 메타데이터 저장)
def create_pdf_file(db: Session, pdf_file_data: PdfContentCreateDB) -> PdfFile:
    """DB에 새로운 PdfFile 객체를 생성하고 저장합니다."""
    
    # PdfFileUpload 스키마에서 받은 데이터를 기반으로 DB 모델 인스턴스 생성
    db_pdf = PdfFile(**pdf_file_data.model_dump())
    
    db.add(db_pdf)
    db.commit()      # DB에 변경사항 적용
    db.refresh(db_pdf) # 자동 생성된 id와 public_id를 객체에 다시 로드
    
    return db_pdf

# READ (public_id로 단일 조회)
def get_pdf_file_by_public_id(db: Session, public_id: str) -> Optional[PdfFile]:
    """public_id를 기준으로 PdfFile 객체를 조회합니다."""
    
    return db.query(PdfFile).filter(PdfFile.public_id == public_id).first()

# READ (내부 ID로 단일 조회 - FK 참조용)
def get_pdf_file_by_id(db: Session, pdf_id: int) -> Optional[PdfFile]:
    """내부 ID를 기준으로 PdfFile 객체를 조회합니다."""
    
    return db.query(PdfFile).filter(PdfFile.id == pdf_id).first()