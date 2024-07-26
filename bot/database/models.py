from sqlalchemy import BigInteger, Column, Integer
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


class User(BaseModel):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
