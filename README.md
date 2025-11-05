

8002번 포트로 실행

uv run uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8002


# env 파일 예시

APP_NAME="My FastAPI Service"
ENVIRONMENT="development"
HOST="0.0.0.0"
PORT=8002

SECRET_KEY="SOME_VERY_LONG_AND_RANDOM_SECRET" # 아직 추가 안함