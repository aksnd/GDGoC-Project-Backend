from pydantic import BaseModel, Field
from typing import Optional

# 2. PUT /archive/{id} 입력 스키마 (수정 요청)
class ArchivingContentUpdate(BaseModel):
    """
    기존 아카이빙 내용을 수정할 때 사용되는 스키마.
    content 필드만 필수적으로 업데이트합니다.
    """
    
    # ⭐ 텍스트 내용: 수정의 핵심이므로 필수(Required)로 설정
    content: str = Field(..., description="수정할 아카이빙 내용 텍스트")
    
    # 이 스키마는 content만 받으며, image_url 등 다른 필드는 포함하지 않습니다.
    # 따라서 API나 Service 계층에서는 image_path를 변경하지 않도록 로직을 구현합니다.
    
class ArchiveContentCreateDB(BaseModel):
    # ⭐ 주의: FK인 pdf_id는 services에서 찾아서 넘겨주어야 합니다.
    pdf_id: int
    page_number: int
    content: str
    source_type: str
    image_path: Optional[str] = None