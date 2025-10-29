from fastapi import FastAPI
from .core.config import settings

# FastAPI 인스턴스를 'app' 이라는 이름으로 정확하게 정의해야 합니다.
app = FastAPI() 

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

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
# 다른 라우트나 설정 코드가 뒤따를 수 있습니다.
# ...