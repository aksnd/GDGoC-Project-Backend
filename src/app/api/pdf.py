# src/app/api/pdf.py

from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.pdf import create_pdf_project, get_pdf_data_by_id
from ..crud.crud_pdf_file import get_pdf_files_by_user
from ..schemas.pdf import PdfFileResponse 
from typing import List


router = APIRouter(
    prefix="/pdfs",
    tags=["PDF Management"]
)

# 예시: POST /pdfs/upload - PDF 메타데이터 등록
@router.post("/upload", response_model=PdfFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf_info(
    pdf_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    [API Layer] PDF 파일의 메타데이터를 등록하고 public_id를 반환합니다. 
    로직은 services/pdf.py로 위임합니다.
    """
    if pdf_file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF is allowed.")
    
    pdf_response = await create_pdf_project(db, pdf_file)
    
    return pdf_response

@router.get("/my_pdfs", response_model=List[PdfFileResponse])
def load_user_pdf_info(
    user_id: str, 
    db: Session = Depends(get_db)
):
    """
    [API Layer] 요청된 user_id에 해당하는 모든 PDF 메타데이터 목록을 조회합니다.
    """
    
    # 특정 사용자 PDF 조회 CRUD 함수 호출
    user_pdfs_db_instances = get_pdf_files_by_user(db, user_id=user_id)
    
    return user_pdfs_db_instances

# 예시: GET /pdfs/{public_id} - 프로젝트 로드
@router.get("/{public_id}")
def load_pdf_by_id(public_id: str, db: Session = Depends(get_db)):
    """
    [API Layer] 특정 public_id로 PDF를 로드합니다.
    """
    pdf_response = get_pdf_data_by_id(db, public_id)
    
    return FileResponse(
        path = pdf_response.file_path,
        media_type="application/pdf",
        filename=pdf_response.filename,
    )
    
