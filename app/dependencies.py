"""
- 예제 단순화를 위한 커스텀 헤더를 사용한다.
- 실제로는 보안, 인증 및 권한 부여를 처리하기 위한 apiKey, http, oauth2, openIdConnect 등의
  통합된 [Security utilites](https://fastapi.tiangolo.com/tutorial/security/)를 사용해야 한다.
- TODO: JWT token 사용하여 공통 인증 서비스 연동
"""
import os
from typing import Annotated

from fastapi import Header
from starlette import status

import app.models as models
from app import SERVICE_CODE
from app.database import SessionLocal, engine
from app.exceptions import CustomHTTPError

DEFAULT_X_TOKEN = os.getenv('DEFAULT_X_TOKEN', "fake-super-secret-token")


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != DEFAULT_X_TOKEN:
        raise CustomHTTPError(
            code=int(str(SERVICE_CODE) + str(status.HTTP_401_UNAUTHORIZED)),
            message="Invalid x-token header", result={}
        )


models.Base.metadata.create_all(bind=engine)  # type: ignore


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
