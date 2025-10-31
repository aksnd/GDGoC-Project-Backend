# init_db.py (프로젝트 루트 디렉토리에 위치)

import os
import sys

# 1. Python 경로 설정: 프로젝트의 src/app/ 경로를 인식하도록 설정
# 이 부분이 없으면 from src.app.models/db 임포트가 실패합니다.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.app.db.database import engine, Base 
import src.app.models 

def initialize_database():
    """
    Base에 정의된 모든 모델을 기반으로 SQLite DB에 테이블을 생성합니다.
    (테이블이 이미 존재하면 건너뜁니다.)
    """
    print("--- 🔨 DB 스키마 초기화를 시작합니다. ---")
    
    # SQLAlchemy의 핵심 기능: Base에 등록된 모든 메타데이터(모델)를 DB 엔진에 바인딩하여 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    print("--- ✅ DB 스키마 초기화 완료 ---")
    
    print("\n--- 📋 생성된 테이블 목록 ---")
    
    # 3. Base.metadata에 등록된 테이블 이름만 출력
    for table in Base.metadata.sorted_tables:
        print(f"- {table.name}")
        
    print("----------------------------")


if __name__ == "__main__":
    initialize_database()