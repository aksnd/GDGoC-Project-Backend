# src/app/api/pdf.py

from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.pdf import create_pdf_project, get_project_data
from ..schemas.pdf import PdfFileResponse 

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

# 예시: GET /pdfs/{public_id} - 프로젝트 로드
@router.get("/{public_id}", response_model = PdfFileResponse)
def load_project_by_id(public_id: str, db: Session = Depends(get_db)):
    """
    [API Layer] 특정 public_id로 프로젝트 정보를 로드합니다.
    """
    pdf_response = get_project_data(db, public_id)
    
    return pdf_response