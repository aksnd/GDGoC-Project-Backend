# src/app/crud/crud_archiving_content.py

from sqlalchemy.orm import Session
from ..models.archiving_content import ArchivingContent
from ..schemas.archive import ArchiveContentCreateDB
from typing import Optional

# CREATE (새 아카이빙 내용 저장)
def create_archiving_content(db: Session, archive_file_data = ArchiveContentCreateDB) -> ArchivingContent:
    """새 아카이빙 내용을 DB에 저장합니다."""
    
    db_content = ArchivingContent(**archive_file_data.model_dump())
    
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    
    return db_content

# READ (ID로 단일 조회)
def get_archiving_content_by_id(db: Session, content_id: int) -> Optional[ArchivingContent]:
    """아카이빙 내용 ID를 기준으로 객체를 조회합니다."""
    
    return db.query(ArchivingContent).filter(ArchivingContent.id == content_id).first()

# UPDATE (내용 수정)
def update_archiving_content(
    db: Session, 
    db_content: ArchivingContent, 
    new_content: str
) -> ArchivingContent:
    """기존 아카이빙 내용의 텍스트(content)를 수정합니다."""
    
    # 텍스트 필드 업데이트
    db_content.content = new_content
    
    # last_modified 필드는 모델의 onupdate 설정에 따라 자동으로 갱신됨
    
    db.commit()
    db.refresh(db_content)
    
    return db_content

# DELETE (삭제)
def delete_archiving_content(db: Session, db_content: ArchivingContent) -> None:
    """아카이빙 내용을 DB에서 삭제합니다 (Hard Delete)."""
    
    db.delete(db_content)
    db.commit()