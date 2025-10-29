# Python 3.11 환경을 기반으로 시작
FROM python:3.11-slim

# 작업 디렉토리를 /app으로 설정
WORKDIR /app

# uv 설치 (pip이 있다면 uv를 설치합니다)
RUN pip install uv

# pyproject.toml 파일을 복사하고 의존성을 설치합니다.
# 이 두 라인이 캐싱에 유리하여 빌드 속도를 높입니다.
COPY pyproject.toml .
RUN uv sync

# 나머지 프로젝트 코드를 복사합니다.
COPY . .

# FastAPI가 사용할 8002번 포트를 외부에 노출합니다.
EXPOSE 8002

# 서버 실행 명령어 (컨테이너가 시작될 때 실행됩니다)
CMD ["/usr/local/bin/python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8002"]