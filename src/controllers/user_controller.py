from fastapi import APIRouter, HTTPException, Depends
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.user_schema import UserLogin, RefreshToken, UserBase
from src.services.user_service import social_login, social_login_or_register
from src.utils.jwt_utils import get_access_token_by_refresh_token

router = APIRouter()


@router.post("/users/login", response_model=dict, dependencies=[Depends(get_db)])
async def login_user(user_base: UserBase, db: Session = Depends(get_db)):
    try:
        tokens, status_code = social_login_or_register(user_base, db)
        return JSONResponse(content=tokens, status_code=status_code)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/users/refresh", response_model=dict)
async def get_new_access_token(refresh_token: RefreshToken):
    try:
        tokens = get_access_token_by_refresh_token(refresh_token.refresh_token)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
