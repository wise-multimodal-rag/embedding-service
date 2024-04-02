import json
import logging
import os
import sys
import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.config import settings
from app.dependencies import get_token_header
from app.docs.main import description
from app.log import setup_logging
from app.routers import embedding
from app.src.exception.service import SampleServiceError
from app.version import GIT_REVISION, GIT_BRANCH, BUILD_DATE, GIT_SHORT_REVISION, VERSION, get_current_datetime

# 앱 구동 성공 여부와 상관없이 앱 정보 출력
print(json.dumps(
    {"SERVICE NAME": settings.SERVICE_NAME, "SERVICE CODE": settings.SERVICE_CODE, "SERVICE VERSION": VERSION,
     "HOME_PATH": os.getcwd(), "COMMAND": ' '.join(sys.argv),
     "Usage": "uvicorn app.main:app --host 0.0.0.0 --port <port number>"}, ensure_ascii=False))


@asynccontextmanager
async def lifespan(lifespan_app: FastAPI):
    # startup event
    logging.info(f"uptime: {get_current_datetime()}")
    logging.debug(f"Working Directory: {repr(os.getcwd())}")
    logging.info(f"Start {settings.SERVICE_NAME} {VERSION}")
    yield
    # shutdown event
    logging.info(f"Shut down {settings.SERVICE_NAME} Service")


app = FastAPI(
    lifespan=lifespan,
    title=f"{settings.SERVICE_NAME} Service",
    summary="Embedding Service 🚀",
    description=description,
    version=VERSION,
    license_info={
        "name": "Wisenut"
    },
    dependencies=[Depends(get_token_header)]
)
app.logger = setup_logging()  # type: ignore

app.include_router(embedding.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.6f} sec"
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(str(settings.SERVICE_CODE) + str(exc.status_code)),
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
            "code": int(f"{settings.SERVICE_CODE}{status.HTTP_422_UNPROCESSABLE_ENTITY}"),
            "message": f"Invalid Request: {exc.errors()[0]['msg']} (type: {exc.errors()[0]['type']}), "
                       f"Check {(exc.errors()[0]['loc'])}",
            "result": {
                "body": exc.body
            }
        }
    )


@app.exception_handler(ValidationError)
async def request_validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(str(settings.SERVICE_CODE) + str(status.HTTP_422_UNPROCESSABLE_ENTITY)),
            "message": "pydantic model ValidationError 발생",
            "result": {
                "body": exc.errors()
            }
        }
    )


@app.exception_handler(SampleServiceError)
async def embedding_exception_handler(request: Request, exc: SampleServiceError):
    logging.error(f"{request.client} {request.method} {request.url} → {repr(exc)}")
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
    return {"title": app.title, "summary": app.summary, "version": app.version, "docs_url": app.docs_url}


@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": settings.SERVICE_NAME,
        "version": VERSION,
        "home_path": os.getcwd(),
        "command": f"{' '.join(sys.argv)}",
        "build_date": BUILD_DATE,
        "uptime": get_current_datetime()
    }


@app.get("/info")
async def info():
    version: str = VERSION
    if 'Unknown' in version:
        version = version.split('.')[0]
    return {
        "service": settings.SERVICE_NAME,
        "version": version,
        "git_branch": GIT_BRANCH,
        "git_revision": GIT_REVISION,
        "git_short_revision": GIT_SHORT_REVISION,
        "build_date": BUILD_DATE,
        "uptime": get_current_datetime()
    }


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == '__main__':
    uvicorn.run(app="main:app", host="0.0.0.0", port=settings.PORT, log_level=settings.SYSTEM_LOG_LEVEL)
