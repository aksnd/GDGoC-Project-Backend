from fastapi import FastAPI

# FastAPI 인스턴스를 'app' 이라는 이름으로 정확하게 정의해야 합니다.
app = FastAPI() 

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# 다른 라우트나 설정 코드가 뒤따를 수 있습니다.
# ...