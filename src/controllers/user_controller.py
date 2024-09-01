from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.auth.auth import JWTBearer
from src.config.database import get_db
from src.services.user_service import create_user, social_login, get_access_token_by_refresh_token
from src.schemas.user_schema import UserCreate, UserBase, UserLogin, RefreshToken

router = APIRouter()


@router.post("/users/signup", response_model=UserCreate, status_code=201, dependencies=[Depends(JWTBearer())])
async def signup_user(user_data: UserBase):
    try:
        user = create_user(user_data)
        return user
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/users/login", response_model=dict)
async def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    try:
        tokens = social_login(user_login.social_id, db)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/users/refresh", response_model=dict)
async def get_new_access_token(refresh_token: RefreshToken):
    try:
        tokens = get_access_token_by_refresh_token(refresh_token.refresh_token)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
