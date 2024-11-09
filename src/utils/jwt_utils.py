import jwt
from datetime import datetime, timedelta
from src.config.settings import JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from src.utils.error_codes import ErrorDetails


def get_new_token(social_id: str) -> dict[str, str]:
    access_token = create_access_token({"sub": social_id})
    secret_token = create_secret_token({"sub": social_id})

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


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def create_secret_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        return None
