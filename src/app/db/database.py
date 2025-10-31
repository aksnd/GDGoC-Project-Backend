# src/app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.app.core.config import settings

# DB 엔진 생성
# check_same_thread=False는 SQLite의 동시성 문제 회피를 위해 FastAPI에서 필요합니다.
engine = create_engine(
     settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 모델의 기반이 되는 클래스
Base = declarative_base()

# DB 세션을 얻기 위한 의존성 주입 함수 (FastAPI에서 사용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()