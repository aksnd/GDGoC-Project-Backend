from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
import uuid
from pathlib import Path 
from typing import Tuple
import fitz  # PyMuPDF

# ⭐ CRUD 및 Schemas 임포트
from ..crud import crud_pdf_file 
from ..schemas.pdf import PdfContentCreateDB, PdfFileResponse 
from ..models.pdf_file import PdfFile

# Ensure storage directories exist
PDF_STORAGE_DIR = Path("files") / "pdfs"
PDF_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_IMAGE_DIR = Path("files") / "profile_images"
PROFILE_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------

def save_first_page_as_image(pdf_path: str, output_image_path: str, resolution: int = 200) -> bool:
    """
    PDF 파일의 첫 번째 페이지를 이미지로 저장합니다.

    Args:
        pdf_path (str): 원본 PDF 파일의 경로.
        output_image_path (str): 저장될 이미지 파일의 경로 (예: "output.png" 또는 "output.jpg").

    Returns:
        bool: 이미지가 성공적으로 저장되었으면 True, 실패했으면 False를 반환합니다.
    """
    try:
        # PDF 문서 열기
        doc = fitz.open(pdf_path)
        
        # 첫 번째 페이지 가져오기 (인덱스는 0부터 시작)
        page = doc[0]
        
        # 페이지를 Pixmap으로 렌더링
        pix = page.get_pixmap(matrix=fitz.Matrix(resolution/72, resolution/72))
        
        # Pixmap을 이미지 파일로 저장
        pix.save(output_image_path)
        doc.close()
        return True
    except Exception as e:
        print(f"Error saving first page of PDF as image from '{pdf_path}' to '{output_image_path}': {e}")
        return False

async def _save_file_to_storage(pdf_file: UploadFile, public_id: str) -> str:
    """
    PDF 파일을 GCS에 저장하고, 저장된 경로를 반환합니다.
    """
    # 1. 파일 저장 경로 및 이름 생성
    file_extension = Path(pdf_file.filename).suffix.lower()
    if file_extension != '.pdf':
         raise HTTPException(status_code=400, detail="Only PDF files are supported.")
         
    safe_filename = f"{public_id}_{uuid.uuid4().hex}{file_extension}"
    file_path_on_disk = PDF_STORAGE_DIR / safe_filename
    
    try:
        # FastAPI의 UploadFile 내용을 비동기적으로 읽어 파일에 씁니다.
        file_content = await pdf_file.read() 
        
        # 파일 쓰기는 blocking I/O이므로 ThreadPoolExecutor를 사용하거나 (간결함을 위해 생략)
        # 일반 open/write를 사용합니다.
        with open(file_path_on_disk, "wb") as f:
            f.write(file_content)
            
        # 3. DB에 기록할 상대 경로와 페이지 수 (가정) 반환
        # DB에는 절대 경로 대신, 프로젝트 루트를 기준으로 한 상대 경로를 저장합니다.
        db_file_path = str(file_path_on_disk)
        
        return db_file_path
    except Exception as e:
        # 파일 저장 중 오류 발생 시 500 에러
        raise HTTPException(status_code=500, detail=f"Local file storage error: {e}")


# ------------------------------------------------------------------
# 2. 핵심 서비스 함수: PDF 파일 처리 및 DB 등록
# ------------------------------------------------------------------

async def create_pdf_project(
    db: Session,
    pdf_file: UploadFile,
    user_id: str,
) -> PdfFileResponse:
    """
    [Service Layer]
    1. 파일을 저장소에 업로드합니다.
    2. PDF 첫 페이지를 이미지로 저장합니다.
    3. 메타데이터를 DB에 기록하고 public_id를 포함한 응답 스키마를 반환합니다.
    """

    # 1. public_id 생성 (DB 모델에서 생성되지만, 파일 이름에 사용하기 위해 미리 생성)
    # 💡 DB 모델의 default 함수를 직접 호출하여 public_id를 생성합니다.
    public_id = str(uuid.uuid4())

    # 2. 파일 저장소에 업로드 및 최종 경로 획득
    final_file_path = await _save_file_to_storage(pdf_file, public_id)

    # 3. PDF 첫 페이지를 이미지로 저장
    profile_image_path = None
    try:
        # 이미지 파일명 생성 (public_id를 사용하여 PDF와 동일한 식별자 사용)
        image_filename = f"{public_id}_thumbnail.png"
        image_path_on_disk = PROFILE_IMAGE_DIR / image_filename

        # PDF 첫 페이지를 이미지로 저장
        if save_first_page_as_image(str(final_file_path), str(image_path_on_disk)):
            profile_image_path = str(image_path_on_disk)
        else:
            # 이미지 저장 실패 시 로그 출력 (에러는 발생시키지 않음)
            print(f"Warning: Failed to generate thumbnail for PDF {public_id}")
    except Exception as e:
        # 썸네일 생성 실패가 전체 프로세스를 중단시키지 않도록 처리
        print(f"Warning: Error generating thumbnail for PDF {public_id}: {e}")

    # 4. DB CREATE 스키마 구성 (CRUD 호출용)
    db_data = PdfContentCreateDB(
        filename= pdf_file.filename,
        file_path= final_file_path,
        profile_image_path= profile_image_path,
        user_id = user_id,
        public_id =public_id,
    )

    # 5. CRUD 호출 및 DB에 저장
    db_pdf_instance: PdfFile = crud_pdf_file.create_pdf_file(db, pdf_file_data=db_data)

    # 6. 응답 모델로 변환하여 반환
    return PdfFileResponse.model_validate(db_pdf_instance)

# ------------------------------------------------------------------
# 3. 추가 서비스 함수: 특정 프로젝트 정보 로드
# ------------------------------------------------------------------

def get_pdf_data_by_id(db: Session, public_id: str) -> PdfFile:
    """
    [Service Layer] public_id를 사용하여 DB에서 프로젝트 메타데이터를 조회합니다.
    (나중에 Chat History와 Archiving Content 로직이 여기에 추가됩니다.)
    """
    db_pdf = crud_pdf_file.get_pdf_file_by_public_id(db, public_id)
    
    if not db_pdf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project not found with ID: {public_id}")
        
    return PdfFileResponse.model_validate(db_pdf)