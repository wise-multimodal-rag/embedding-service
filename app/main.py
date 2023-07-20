import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app import conf, LOG_LEVEL, VERSION, GIT_BRANCH, GIT_REVISION, GIT_SHORT_REVISION, BUILD_DATE, SERVICE_CODE
from app.dependencies import get_token_header
from app.exceptions import CustomHTTPError
from app.internal import admin
from app.log import setup_logging
from app.routers import items, users


def check_env_exist() -> None:
    """
    설정이 필요한 환경변수가 세팅되어있는지 체크
    TODO: 필요한 환경변수가 없을 경우, 프로그램 종료

    Returns: None

    """
    env_list = ['DEFAULT_TOKEN']  # TODO: 확인할 환경변수 설정
    for env in env_list:
        if env not in os.environ.keys():
            logging.warning(f"set {repr(env)} environment variable.")


@asynccontextmanager
async def lifespan(lifespan_app: FastAPI):
    # startup event
    logging.debug(f"Working Directory: {repr(os.getcwd())}")
    logging.info("Start Python FastAPI Template")
    logging.info("Check env exist ...")
    check_env_exist()
    yield
    # shutdown event
    logging.info("Shut down Python FastAPI Template")


app = FastAPI(
    lifespan=lifespan,
    title="Python FastAPI Template",
    description="DE Team Python FastAPI Template",
    version=VERSION,
    dependencies=[Depends(get_token_header)]
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,  # app/internal/admin.py 원본을 수정하지 않고 선언 가능
    prefix="/admin",
    tags=["admin"],
    responses={418: {"description": "I'm a teapot"}},
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(str(SERVICE_CODE) + str(exc.status_code)),
            "message": f"{exc.detail}",
            "result": {
                "headers": exc.headers
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(str(SERVICE_CODE) + str(status.HTTP_422_UNPROCESSABLE_ENTITY)),
            "message": f"유효하지 않은 요청값 ({exc.errors()[0]['msg']}), "
                       f"{(exc.errors()[0]['loc'][0], exc.errors()[0]['loc'][1])}을 확인해주세요.",
            "result": {
                "body": exc.body
            }
        }
    )


@app.exception_handler(CustomHTTPError)
async def custom_exception_handler(request: Request, exc: CustomHTTPError):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(exc.code),
            "message": f"{exc.message}",
            "result": exc.result
        }
    )


@app.get("/")
async def root():
    return {"title": app.title, "description": app.description, "version": app.version, "docs_url": app.docs_url}


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.get("/info")
async def info():
    version: str = VERSION
    if 'Unknown' in version:
        version = version.split('.')[0]
    return {
        "version": version,
        "git_branch": GIT_BRANCH,
        "git_revision": GIT_REVISION,
        "git_short_revision": GIT_SHORT_REVISION,
        "build_date": BUILD_DATE
    }


# setup logging last, to make sure no library overwrites it
# (they shouldn't, but it happens)
setup_logging()

if __name__ == "__main__":
    if 'PORT' in conf.keys():
        port = int(conf['PORT'])
    else:
        port = 8000

    uvicorn.run(app="main:app", host="0.0.0.0", port=port, log_level=LOG_LEVEL)
