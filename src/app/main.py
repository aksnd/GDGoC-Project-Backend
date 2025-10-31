from fastapi import FastAPI
from .core.config import settings
import sqlite3

# FastAPI 인스턴스를 'app' 이라는 이름으로 정확하게 정의해야 합니다.
app = FastAPI() 

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI! with CI/CD"}

@app.get("/config-test")
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

@app.get("/db-test")
def check_db_connection():
    """
    SQLite DB 파일의 연결 상태를 확인하고 정보를 반환합니다.
    """
    
    conn = sqlite3.connect(settings.DATABASE_URL)
    cur = conn.cursor()
    
    # SQLite 버전 확인
    cur.execute("SELECT sqlite_version();")
    sqlite_version = cur.fetchone()[0]
    
    conn.close()
    return {
        "database_url": settings.DATABASE_URL,
        "sqlite_version": sqlite_version,
    }
    
