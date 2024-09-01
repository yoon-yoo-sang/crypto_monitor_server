from sqlalchemy.orm import Session

from src.models.user import User
from src.schemas.user_schema import UserBase, UserCreate
from src.config.database import SessionLocal
from src.utils.jwt_utils import create_access_token, create_secret_token, verify_token


def create_user(user_data: UserBase) -> UserCreate:
    db = SessionLocal()
    try:
        # 사용자 중복 체크
        existing_user = db.query(User).filter(User.social_id == user_data.social_id).first()
        if existing_user:
            raise Exception("User already exists with this social ID")

        # 새로운 사용자 생성
        new_user = User(
            social_id=user_data.social_id,
            username=user_data.username,
            email=user_data.email
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # 응답 모델로 변환
        return UserCreate(
            id=new_user.id,
            created_at=new_user.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            username=new_user.username,
            email=new_user.email
        )
    finally:
        db.close()


def social_login(social_id: str, db: Session):
    # 사용자 조회
    user = db.query(User).filter(User.social_id == social_id).first()

    if not user:
        raise ValueError("Invalid social ID")

    # 토큰 생성
    access_token = create_access_token({"sub": user.social_id})
    secret_token = create_secret_token({"sub": user.social_id})

    return {
        "access_token": access_token,
        "secret_token": secret_token
    }


def get_access_token_by_refresh_token(refresh_token: str):
    if not verify_token(refresh_token):
        raise ValueError("Invalid token")

    # 토큰 생성
    access_token = create_access_token({"sub": refresh_token})

    return {
        "access_token": access_token
    }
