# src/app/api/chat.py

import os
import uuid
import google.generativeai as genai
from google.generativeai import types as genai_types
from fastapi import APIRouter, Depends, status, File, UploadFile, Form, HTTPException 
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..crud import crud_chat_history, crud_pdf_file
from ..schemas.chat_history import ChatHistoryCreateDB
from ..services.pdf import get_pdf_data_by_id
from fastapi.responses import FileResponse

# 💡 TODO: schemas, services 모듈은 추후 완성됩니다.

# Configure Gemini API
try:
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    if not GEMINI_API_KEY:
        raise ValueError("Error: Cannot find GEMINI_API_KEY environment variable.")
    
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash') 
    print("Gemini Model (gemini-2.5-flash) loaded successfully.")

except ValueError as e:
    print(e)
    model = None
except Exception as e:
    print(f"Unexpected error occurred while loading Gemini model: {e}")
    model = None

router = APIRouter(
    prefix="/chat",
    tags=["Chat & History"]
)

# 예시: POST /chat/query - Gemini 질의 및 기록 저장
@router.post("/query")
async def process_chat_query(
    image_file: UploadFile = File(..., description="드래그한 이미지 파일"),
    public_id: str = Form(..., description= "pdf의 공개 id"),
    page_number: int = Form(..., description= "질문이 발생한 PDF 페이지 번호"),
    question_query: str = Form(..., description= "질문 query"),
    db: Session = Depends(get_db),
):
    """
    [API Layer] 사용자 질문, 페이지 정보를 받아 Gemini에게 질의하고 기록을 저장합니다.
    """
    if not model:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Gemini API가 설정되지 않았습니다. 서버 로그에서 GEMINI_API_KEY를 확인하세요."
        )
    
    if not image_file.content_type or not image_file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"잘못된 파일 타입입니다. 이미지만 업로드 가능합니다. (전송된 타입: {image_file.content_type})"
        )
    
    try:
        image_bytes = await image_file.read()

        image_part = {
            'mime_type': image_file.content_type,
            'data': image_bytes
        }

        full_prompt = f"""
        첨부된 이미지에 대한 사용자의 질문입니다:
        "{question_query}"

        이미지와 컨텍스트를 바탕으로 질문에 답해주세요.
        """

        response = await model.generate_content_async(
            contents=[image_part, full_prompt]
        )

        answer = response.text

        # Save to DB
        pdf_file_db = crud_pdf_file.get_pdf_file_by_public_id(db, public_id=public_id)
        if not pdf_file_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 public_id를 가진 PDF를 찾을 수 없습니다.")

        IMAGE_DIR = "files/images"
        os.makedirs(IMAGE_DIR, exist_ok=True)
        
        file_extension = os.path.splitext(image_file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        image_path = os.path.join(IMAGE_DIR, unique_filename)
        
        with open(image_path, "wb") as buffer:
            buffer.write(image_bytes)

        chat_history_to_db = ChatHistoryCreateDB(
            pdf_id=pdf_file_db.id,
            page_number=page_number,
            question_query=question_query,
            response_query=answer,
            image_path=image_path
        )
        
        crud_chat_history.create_chat_entry(db=db, chat_history_data=chat_history_to_db)

        return {
            "answer": answer,
            "context": {
                "public_id": public_id,
                "page_number": page_number,
                "question": question_query
            }
        }
    
    except genai_types.generation_types.StopCandidateException as e:
        # Gemini API의 안전 설정 (Safety Settings) 등에 의해 차단된 경우
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Gemini API가 안전상의 이유로 요청을 차단했습니다: {e}"
        )
    
    except Exception as e:
        # 기타 예외 처리 (API 키 인증 실패, 네트워크 오류 등)
        print(f"Gemini API 처리 중 오류 발생: {e}") # 서버 로그에 상세 오류 출력
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gemini API 처리 중 오류가 발생했습니다: {str(e)}"
        )

# GET /chat/history/{public_id} - 해당 PDF 질의 기록 전체 불러오기
@router.get("/history/{public_id}")
def load_history_by_id(public_id: str, db: Session = Depends(get_db)):
    """
    [API Layer] 특정 public_id로 해당 PDF의 chat history들을 로드합니다.
    """
    pdf_id = crud_pdf_file.get_pdf_file_by_public_id(db, public_id).id
    print(pdf_id)
    chat_histories = crud_chat_history.get_chat_history_by_pdf_id(db, pdf_id)
    
    return chat_histories

# GET /chat/image/{chat_history_id} - 해당 PDF의 특정 질의 기록의 이미지 불러오기
@router.get("/image/{chat_history_id}")
def load_image_by_chat_history_id(chat_history_id, db:Session = Depends(get_db)):
    """
        chat_history_id로 해당 chat으로 넣은 사진을 로드합니다.
    """
    chat_response = crud_chat_history.get_chat_history_by_id(db, chat_history_id)
    
    return FileResponse(
        path = chat_response.image_path,
        media_type= "image/png",
        filename =f"{chat_history_id}_image.png",
    )
    
    
    
    
    
    