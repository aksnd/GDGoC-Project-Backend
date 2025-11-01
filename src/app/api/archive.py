# src/app/api/archive.py
from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Optional

from ..db.database import get_db
from ..schemas.archive import ArchivingContentUpdate


# 💡 TODO: schemas, services 모듈은 추후 완성됩니다.

router = APIRouter(
    prefix="/archive",
    tags=["Archiving Content Management"]
)

# 예시: POST /archive - 새 아카이빙 내용 추가
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_archive_content(
    # 파일 데이터 (선택적)
    image_file: Optional[UploadFile] = File(None, description="선택적 아카이빙 이미지 파일"),
    
    # 텍스트 데이터 (Form으로 받음)
    public_id: str = Form(..., description="메모를 저장할 PDF 프로젝트의 공개 ID"),
    page_number: int = Form(..., description="메모가 속한 PDF 페이지 번호"),
    content: str = Form(..., description="사용자가 입력한 아카이빙 내용"),
    
    db: Session = Depends(get_db)
):
    """
    [API Layer] 새로운 아카이빙 내용(메모)과 선택적 이미지 파일을 받습니다.
    """
    # ⭐ DB 저장 및 return 로직은 나중에 구현
    # db_content = await create_archive_content_service(db, public_id, ...)
    # return db_content 
    
    return {"message": "Archive creation request received."}

# --------------------------
# 2. UPDATE (PUT) - 텍스트 내용 수정
# --------------------------
@router.put("/{content_id}")
def update_archive_content(
    content_id: int, 
    content_schema: ArchivingContentUpdate,
    db: Session = Depends(get_db),
):
    """
    [API Layer] 기존 아카이빙 내용을 수정합니다.
    """
    # ⭐ DB 수정 및 return 로직은 나중에 구현
    # content = update_archive_content_service(db, content_id, update_data)
    # return content

    return {"message": f"Archive content {content_id} update request received."}

# --------------------------
# 3. DELETE (DELETE) - 내용 삭제
# --------------------------
@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_archive_content(
    content_id: int, 
    db: Session = Depends(get_db)
):
    """
    [API Layer] 특정 아카이빙 내용을 삭제합니다.
    """
    # ⭐ DB 삭제 로직은 나중에 구현
    # success = delete_archive_content_service(db, content_id)
        
    # 204 No Content는 응답 본문이 없음을 의미합니다.
    return