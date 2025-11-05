from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..crud.crud_user import create_user, get_user
from typing import Optional

router = APIRouter(prefix="/users", tags=["Users"])

# ----------------------------------------------------
# 1. 회원가입 API (CREATE USER)
# ----------------------------------------------------
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user_id: str = Body(..., embed=True), 
    password: Optional[str] = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    """새로운 사용자를 생성합니다."""
    
    # 1. 사용자 ID 중복 확인
    db_user = create_user(db, user_id, password)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID already registered"
        )
    
    # 2. 평문 비밀번호로 사용자 생성
    new_user = create_user(db=db, user_id=user_id, password=password)
    
    # 반환 형식은 user_id만 간단하게
    return {"message": "User registered successfully", "user_id": new_user.user_id}

# ----------------------------------------------------
# 2. 사용자 확인/로그인 API (CONFIRM USER)
# ----------------------------------------------------
@router.post("/login")
def login_user(
    user_id: str = Body(..., embed=True), 
    password: Optional[str] = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    """사용자 ID와 비밀번호를 검증하여 로그인합니다."""
    
    # 1. 사용자 객체 조회
    db_user = get_user(db, user_id=user_id)
    
    # 🚨 2. CASE 1: ID가 아예 없는 경우
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # DB 비밀번호가 설정되어 있고 (NULL 아님), 입력 비밀번호와 다를 때
    if db_user.password is not None and db_user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
        
    # DB 비밀번호가 NULL (소셜 로그인 등)인 상태에서, 사용자가 비밀번호를 입력했을 때
    if db_user.password is None and password is not None:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password not set for this account."
        )

    # 4. 로그인 성공 처리
    return {"message": "Login successful", "user_id": user_id}