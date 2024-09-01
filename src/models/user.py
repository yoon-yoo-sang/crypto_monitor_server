from sqlalchemy import Column, String

from src.models.common import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    social_id = Column(String(100), nullable=False, unique=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
