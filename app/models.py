from typing import Any

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app import SERVICE_CODE, VERSION
from app.database import Base
from app.log import Log


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class APIResponseModel(BaseModel):
    """기본 API 응답 포맷 by AIP Restful API 디자인 가이드"""
    code: int = int(f"{SERVICE_CODE}200")
    message: str = f"API Response Success ({VERSION})" if Log.is_debug_enable() else "API Response Success"
    result: dict[str, Any] = {}
    description: str = ""
