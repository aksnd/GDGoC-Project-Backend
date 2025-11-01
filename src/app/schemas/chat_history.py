from pydantic import BaseModel
from typing import Optional

# ... (요청/응답 스키마는 생략) ...

# ⭐ DB CREATE 전용 스키마: 질문/답변 기록에 필요한 필드 포함
class ChatHistoryCreateDB(BaseModel):
    pdf_id: int
    page_number: int
    question_query: str
    response_query: str
    image_path: Optional[str] = None