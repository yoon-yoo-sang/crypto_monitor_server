from pydantic import BaseModel


class UserBase(BaseModel):
    social_id: str
    username: str
    email: str


class UserCreate(BaseModel):
    id: int
    created_at: str
    username: str
    email: str


class UserLogin(BaseModel):
    social_id: str


class RefreshToken(BaseModel):
    refresh_token: str
