from sqlalchemy.orm import Session
from ..models.user import User  # User 모델 임포트 (경로 확인 필요)

# CREATE (새 User 저장)
def create_user(db: Session, user_id: str, password: str):
    """
    새로운 User 레코드를 데이터베이스에 생성합니다.
    """
    # User 객체 생성
    db_user = User(
        user_id=user_id,
        password=password  # ⚠️ 보안 미적용 상태
    )
    
    # 세션에 추가, 커밋, 객체 새로고침
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# 2. 사용자 비밀번호 조회 (비밀번호 검증용)
def get_user_password(db: Session, user_id: str):
    """
    주어진 user_id의 비밀번호를 조회합니다.
    """
    # 특정 user_id를 가진 User 객체를 필터링하여 조회
    user = db.query(User).filter(User.user_id == user_id).first()
    
    # 사용자가 존재하면 password 컬럼 값 반환, 없으면 None 반환
    if user:
        return user.password
    return None