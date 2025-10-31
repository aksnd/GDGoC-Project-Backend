from fastapi import FastAPI
from .api import util
# FastAPI 인스턴스를 'app' 이라는 이름으로 정확하게 정의해야 합니다.
app = FastAPI() 

app.include_router(util.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI! with CI/CD"}
