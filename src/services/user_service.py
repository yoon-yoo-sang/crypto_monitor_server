from typing import Tuple

from sqlalchemy.orm import Session

from src.config.database import SessionLocal
from src.models.user import User
from src.schemas.user_schema import UserBase, UserCreate
from src.utils.error_codes import ErrorDetails
from src.utils.jwt_utils import get_new_token


def social_login_or_register(user_data: UserBase, db: Session) -> Tuple[dict[str, str], int]:
    try:
        return social_login(user_data.social_id, db), 200
    except ValueError as e:
        if str(e) == ErrorDetails.USER_NOT_FOUND.value["message"]:
            new_user = create_user(user_data)
            return get_new_token(new_user.social_id), 201
        else:
            print(e)
            raise e


def create_user(user_data: UserBase) -> UserCreate:
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.social_id == user_data.social_id).first()
        if existing_user:
            raise Exception(ErrorDetails.USER_ALREADY_EXISTS.value["message"])

        new_user = User(
            social_id=user_data.social_id,
            username=user_data.username,
            email=user_data.email
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return UserCreate(
            id=new_user.id,
            social_id=new_user.social_id,
            created_at=new_user.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            username=new_user.username,
            email=new_user.email
        )
    finally:
        db.close()


def social_login(social_id: str, db: Session) -> dict[str, str]:
    # 사용자 조회
    user = db.query(User).filter(User.social_id == social_id).first()

    if not user:
        raise ValueError(ErrorDetails.USER_NOT_FOUND.value["message"])

    return get_new_token(social_id)
