# src/app/api/util.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import inspect
from ..db.database import get_db, Base
from ..core.config import settings

# 라우터 객체 생성
router = APIRouter(
    prefix="/util",
    tags=["System Utilities"]
)

@router.get("/config-test")
def get_config():
    """
    로드된 환경 변수를 확인하는 테스트 엔드포인트
    """
    return {
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "is_secret_key_loaded": bool(settings.SECRET_KEY),
        "secret_key": settings.SECRET_KEY,
    }

@router.get("/db-test")
def check_db_connection(db: Session = Depends(get_db)):
    """
    [API Layer] PostgreSQL DB에 성공적으로 접속되었는지 확인합니다.
    """
    try:
        # 📌 SELECT 1 쿼리 실행
        # DB 연결이 성공하고 쿼리 실행 권한이 있다면, 이 명령은 성공적으로 완료됩니다.
        db.execute(text("SELECT 1"))
        
        return {
            "status": "Success",
            "message": "PostgreSQL connection is active and ready.",
            "db_type": "PostgreSQL"
        }
    
    except Exception as e:
        # 쿼리 실행 중 오류가 발생하면 (주로 연결 문제) 실패 반환
        return {
            "status": "Failure",
            "message": f"PostgreSQL connection failed: {e}",
            "db_type": "PostgreSQL"
        }

@router.get("/db-tables")
def get_actual_db_tables(db: Session = Depends(get_db)):
    """
    SQLite 파일에 실제로 존재하는 모든 테이블 목록을 조회합니다.
    """
    try:
        # 1. SQLAlchemy Inspector 객체 생성
        # Inspector는 DB 스키마 정보를 조사하는 데 사용됩니다.
        inspector = inspect(db.bind) # db.bind는 DB 연결 엔진(engine)을 의미합니다.

        # 2. DB에 존재하는 모든 테이블 이름 조회
        table_names = inspector.get_table_names()

        if not table_names:
            return {
                "status": "warning",
                "message": "DB 파일에 테이블이 존재하지 않습니다. init_db.py를 실행했는지 확인하세요."
            }
            
        return {
            "status": "ok",
            "message": f"{len(table_names)}개의 테이블이 DB 파일에 존재합니다.",
            "db_tables": table_names
        }

    except Exception as e:
        # DB 파일이 없거나 손상되었을 경우 에러 처리
        raise HTTPException(
            status_code=500, 
            detail=f"DB 파일에 접근하는 중 오류가 발생했습니다: {e}"
        )