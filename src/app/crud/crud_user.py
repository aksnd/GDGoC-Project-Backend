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

def get_user(db: Session, user_id: str):
    """
    해당 ID를 가진 user가 있는지 확인하여 해당 User 모델 객체를 반환합니다.
    없으면 None을 반환합니다.
    """
    # 📌 User 모델에서 user_id가 일치하는 첫 번째 레코드를 조회
    return db.query(User).filter(User.user_id == user_id).first()