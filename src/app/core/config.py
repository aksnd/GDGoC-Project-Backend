# src/app/core/config.py

from dotenv import load_dotenv # <-- 추가
from pydantic_settings import BaseSettings

# 1. load_dotenv()를 호출하여 .env 파일의 내용을 시스템 환경 변수로 로드
load_dotenv() 

class Settings(BaseSettings):
    # .env 파일에서 읽어올 변수 이름
    APP_NAME: str = "FastAPI App"
    ENVIRONMENT: str = "local"
    # 이제 Pydantic은 load_dotenv()가 로드한 시스템 환경 변수에서 이 값들을 찾습니다.
    SECRET_KEY: str
    PORT: int = 8002

    # model_config은 더 이상 env_file을 지정할 필요가 없습니다.
    # 하지만 변수가 누락되었을 때 Pydantic의 오류 메시지를 명확히 하기 위해 추가 정보는 유지할 수 있습니다.
    # model_config = SettingsConfigDict(extra='ignore') 

# 애플리케이션에서 사용할 설정 인스턴스
settings = Settings()