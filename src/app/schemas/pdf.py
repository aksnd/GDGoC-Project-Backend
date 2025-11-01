from pydantic import BaseModel, Field
from datetime import datetime

class PdfContentCreateDB(BaseModel):
    filename: str = Field(..., max_length=255),
    file_path : str = Field(..., max_length=512),
    
    #default로 생성할 수 도 있지만, 파일이름과의 동기화를 위해 주입하는식으로 구현합니다.
    public_id: str = Field(..., description="Service 계층에서 생성된 고유 ID") 
    
class PdfFileResponse(BaseModel):
    """
    POST /pdfs/upload API의 성공 응답 스키마.
    클라이언트에게 노출되어야 할 필드만 포함합니다.
    """
    public_id: str = Field(..., description="클라이언트가 프로젝트를 식별하는 고유 ID")
    filename: str = Field(..., description="업로드된 파일의 원본 이름")
    file_path: str = Field(..., description="파일이 저장되어 있는 서버 경로")
    upload_time: datetime = Field(..., description="파일이 업로드된 시각 (UTC)")

    model_config = {
        "from_attributes": True
    }