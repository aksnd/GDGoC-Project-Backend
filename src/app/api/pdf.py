# src/app/api/pdf.py

from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..db.database import get_db

# 💡 TODO: schemas, services 모듈은 추후 완성됩니다.

router = APIRouter(
    prefix="/pdfs",
    tags=["PDF Management"]
)

# 예시: POST /pdfs/upload - PDF 메타데이터 등록
@router.post("/upload", status_code=status.HTTP_201_CREATED)
def upload_pdf_info(
    pdf_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    [API Layer] PDF 파일의 메타데이터를 등록하고 public_id를 반환합니다. 
    로직은 services/pdf.py로 위임합니다.
    """
    # db_pdf = process_and_save_pdf(db, pdf_info) # services 호출 (추후 구현)
    
    return {"message": "PDF info received and will be processed."} 

# 예시: GET /pdfs/{public_id} - 프로젝트 로드
@router.get("/{public_id}")
def load_project_by_id(public_id: str, db: Session = Depends(get_db)):
    """
    [API Layer] 특정 public_id로 프로젝트 정보를 로드합니다.
    """
    # project_data = get_project_data(db, public_id) # services 호출 (추후 구현)
    
    return {"public_id": public_id, "status": "Project data loaded."}